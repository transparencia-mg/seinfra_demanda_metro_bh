"""
Atualiza no CKAN só os recursos que mudaram (substitui o `dpckan dataset update`).

Por que este script existe:
  O `dpckan dataset update` só compara o que mudou quando o dataset no CKAN tem
  licença aberta (`isopen`). O nosso não tem, então ele reenvia TODOS os
  recursos a cada execução, recria a estrutura do datastore duas vezes para cada
  um e reenvia o datapackage.json depois de cada recurso. Com 10 meses de ~40 MB,
  uma mudança de uma linha no CHANGELOG levava 4 horas (26/11/2026).

O que faz:
  - arquivo do recurso: compara o MD5 local com o campo `hash` do recurso no
    CKAN (gravado por este script a cada envio). Só reenvia o arquivo (e recria a
    estrutura do datastore) quando o MD5 mudou. Recurso ainda sem `hash` (enviado
    pelo dpckan): baixa o arquivo do CKAN uma vez para comparar; se for igual, só
    grava o `hash`, sem reenviar;
  - nome/descrição do recurso mudaram, mas o arquivo não: só resource_patch;
  - no fim, sempre: datapackage.json remoto e metadados do dataset (README,
    CHANGELOG, título...), uma vez só.

Recursos novos e excluídos são tratados antes pelo scripts/ckan_sync_resources.py.

Uso (variáveis CKAN_HOST e CKAN_KEY no ambiente):
  python scripts/ckan_update_changed.py [--datapackage dataset/datapackage.json]
                                        [--no-datastore] [--simular]
"""
import argparse
import hashlib
import os
import sys
import time
from urllib.request import urlopen

from ckanapi import RemoteCKAN
from dpckan.functions import (
    dataset_patch,
    find_dataset_basepath,
    get_ckan_datapackage_resource_id,
    is_dataset_published,
    load_complete_datapackage,
    resource_update_datastore_metadata,
    update_datapackage_json_resource,
)

from ckan_sync_resources import ler_resources_ids


def md5_arquivo(caminho):
    h = hashlib.md5()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def md5_url(url):
    h = hashlib.md5()
    with urlopen(url, timeout=300) as resp:
        for bloco in iter(lambda: resp.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datapackage", default="dataset/datapackage.json")
    parser.add_argument("--no-datastore", action="store_true")
    parser.add_argument("--simular", action="store_true",
                        help="Só mostra o que seria enviado; não altera nada no CKAN.")
    args = parser.parse_args()
    datastore = not args.no_datastore

    host = os.getenv("CKAN_HOST")
    key = os.getenv("CKAN_KEY")
    if not host or not key:
        print("CKAN_HOST e CKAN_KEY precisam estar definidos.")
        sys.exit(1)

    datapackage = load_complete_datapackage(args.datapackage)
    ckan = RemoteCKAN(host, apikey=key)
    if not is_dataset_published(ckan, datapackage.name):
        print(f"Dataset {datapackage.name} ainda não existe no CKAN; a etapa de criação cuida disso.")
        return

    resources_ids = ler_resources_ids(ckan.action.package_show(id=datapackage.name))
    basepath = find_dataset_basepath(datapackage)
    enviados, so_metadados, iguais = [], [], []

    for nome in datapackage.resource_names:
        if nome not in resources_ids:
            print(f"{nome}: não está em resources_ids (o ckan_sync_resources.py deveria ter criado); pulando.")
            continue
        recurso = datapackage.get_resource(nome)
        resource_id = resources_ids[nome]
        remoto = ckan.action.resource_show(id=resource_id)
        caminho = os.path.join(basepath, recurso.path)
        md5_local = md5_arquivo(caminho)

        md5_remoto = remoto.get("hash") or ""
        if not md5_remoto:
            # enviado pelo dpckan, sem hash: compara baixando o arquivo uma vez
            print(f"{nome}: sem hash no CKAN; baixando para comparar...")
            md5_remoto = md5_url(remoto["url"])
            if md5_remoto == md5_local and not args.simular:
                ckan.call_action("resource_patch", {"id": resource_id, "hash": md5_local})

        titulo = recurso.title or nome
        descricao = recurso.description or ""
        metadados_mudaram = (remoto.get("name") != titulo or (remoto.get("description") or "") != descricao)

        if md5_remoto != md5_local:
            print(f"{nome}: arquivo mudou; enviando {os.path.getsize(caminho) / 1e6:.0f} MB...")
            enviados.append(nome)
            if args.simular:
                continue
            t = time.time()
            with open(caminho, "rb") as arquivo:
                ckan.call_action("resource_update",
                                 {"id": resource_id, "name": titulo, "description": descricao,
                                  "url": recurso.path, "hash": md5_local},
                                 files={"upload": arquivo})
            if datastore:
                resource_update_datastore_metadata(ckan, resource_id, recurso)
            print(f"{nome}: enviado em {(time.time() - t) / 60:.1f} min.")
        elif metadados_mudaram:
            print(f"{nome}: só nome/descrição mudaram; atualizando sem reenviar o arquivo.")
            so_metadados.append(nome)
            if not args.simular:
                ckan.call_action("resource_patch", {"id": resource_id, "name": titulo, "description": descricao})
        else:
            iguais.append(nome)

    if args.simular:
        print(f"SIMULAÇÃO: enviaria {enviados or 'nenhum'}; só metadados {so_metadados or 'nenhum'}.")
        return

    # datapackage.json e metadados do dataset (README, CHANGELOG, título): uma vez só
    update_datapackage_json_resource(ckan, datapackage, get_ckan_datapackage_resource_id(ckan, datapackage.name))
    dataset_patch(ckan, datapackage)
    print(f"Arquivos enviados: {', '.join(enviados) or 'nenhum'}. "
          f"Só metadados: {', '.join(so_metadados) or 'nenhum'}. Sem mudança: {len(iguais)}.")


if __name__ == "__main__":
    main()
