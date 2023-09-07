from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.ContractActions import ContractActions
from Library_v1.LegalOne.ContractJson import ContractJson

class MountData():
    def __init__(self, driver: DriverInterface, json: ContractJson) -> None:
        self.driver = driver
        self.json = json
        self.action = ContractActions(self.driver)
        self.step = 'montar_dados'
        self.json.foreach_contract(self.execute)


    def execute(self, row, data, steps):

        print(f"row: {row}")

        current_step = steps[self.step]
        status = current_step["status"]
        errors = current_step["errors"]

        print(f"self.step: {self.step}")
        print(f"current_step: {current_step}")
        print(f"status: {status}")
        print(f"errors: {errors}")

        # ------------------------------------------------------
        # Verificar se é para executar este passo
        if status != 'EM_ESPERA': return self;
    
        


        return self;