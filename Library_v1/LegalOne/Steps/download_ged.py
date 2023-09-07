from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.ContractActions import ContractActions
from Library_v1.Directory.Directory import Directory
from Library_v1.Utils.file import (
    delete_file,
)

def download_all_ged(driver: DriverInterface) -> list:
    actions = ContractActions(driver)
    download_relativepath = actions.get_download_relativepath()
    # print(f"download_relativepath: {download_relativepath}")

    # -------------------------------------------------
    # Remoção dos arquivos que existe
    files = Directory().find_files(r".*", download_relativepath)
    for file in files: delete_file(file)

    # -------------------------------------------------
    # Downloads dos GEDs
    actions.click_tab('GED')
    ged = actions.read_table_ged()
    for row in ged:
        download_link = row["download_link"]
        actions.navigate_url(download_link)
