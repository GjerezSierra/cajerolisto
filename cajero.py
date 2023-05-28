class Program:
    @staticmethod
    def main(args):
        bancos = Program.crear_bancos()

        print("Bienvenido al Cajero Automático")

        autenticado = False
        intentosRestantes = 4
        cuentaAutenticada = None

        while not autenticado:
            numeroCuenta = input("Ingrese el número de cuenta: ")
            contraseña = input("Ingrese la contraseña: ")

            cuentaAutenticada = Program.autenticar_cliente(bancos, numeroCuenta, contraseña)

            if cuentaAutenticada is not None:
                autenticado = True
            else:
                intentosRestantes -= 1
                print(f"Número de cuenta o contraseña incorrectos. Intentos restantes: {intentosRestantes}")

                if intentosRestantes == 0:
                    print("Ha excedido el número máximo de intentos. Se ha bloqueado la cuenta.")
                    return

        salir = False

        while not salir:
            Program.mostrar_menu()

            opcionStr = input("Seleccione una opción: ")

            if not opcionStr.isdigit():
                print("Opción inválida. Intente nuevamente.")
                continue

            opcion = int(opcionStr)

            print()

            if opcion == 1:
                cuentaAutenticada.consultar_saldo()
            elif opcion == 2:
                try:
                    cuentaAutenticada.realizar_retiro()
                except ValueError as ex:
                    print(ex)
                except RuntimeError as ex:
                    print(ex)
            elif opcion == 3:
                try:
                    cuentaAutenticada.realizar_transferencia(bancos)
                except ValueError as ex:
                    print(ex)
                except RuntimeError as ex:
                    print(ex)
            elif opcion == 4:
                cuentaAutenticada.consultar_puntos_vive_colombia()
            elif opcion == 5:
                try:
                    cuentaAutenticada.canjear_puntos_vive_colombia()
                except ValueError as ex:
                    print(ex)
            elif opcion == 6:
                salir = True
            else:
                print("Opción inválida. Intente nuevamente.")

            print()

        print("¡Gracias por utilizar el Cajero Automático!")

    @staticmethod
    def crear_bancos():
        bancos = []

        # Banco Bancotote
        bancotote = Banco("Bancotote")
        bancotote.registrar_cuenta(Cuenta("901020", "1112", 4000000, 10000))
        bancotote.registrar_cuenta(Cuenta("903050", "1113"))
        bancotote.registrar_cuenta(Cuenta("905090", "1114", 3000000, 40000))
        bancotote.registrar_cuenta(Cuenta("904010", "1115"))
        bancotote.registrar_cuenta(Cuenta("906090", "2030", 5000000, 20000))
        bancos.append(bancotote)

        # Banco Bancolombia
        bancolombia = Banco("Bancolombia")
        bancolombia.registrar_cuenta(Cuenta("905090", "1112", 0, 0))
        bancolombia.registrar_cuenta(Cuenta("802030", "1113"))
        bancolombia.registrar_cuenta(Cuenta("803040", "1114"))
        bancos.append(bancolombia)

        # Banco Davivienda
        davivienda = Banco("Davivienda")
        davivienda.registrar_cuenta(Cuenta("701020", "1112"))
        davivienda.registrar_cuenta(Cuenta("702030", "1113"))
        davivienda.registrar_cuenta(Cuenta("703040", "1112"))
        bancos.append(davivienda)

        # Banco Davinorte
        davinorte = Banco("Davinorte")
        davinorte.registrar_cuenta(Cuenta("601020", "1112", 1000000, 20000))
        davinorte.registrar_cuenta(Cuenta("602030", "1113"))
        davinorte.registrar_cuenta(Cuenta("603040", "1114"))
        bancos.append(davinorte)

        return bancos

    @staticmethod
    def autenticar_cliente(bancos, numeroCuenta, contraseña):
        for banco in bancos:
            cuenta = banco.obtener_cuenta(numeroCuenta)

            if cuenta is not None and cuenta.contraseña == contraseña:
                return cuenta

        return None

    @staticmethod
    def mostrar_menu():
        print("Menú Principal")
        print("1. Consulta de saldo")
        print("2. Retiros")
        print("3. Transferencias")
        print("4. Consulta de puntos ViveColombia")
        print("5. Canje de puntos ViveColombia")
        print("6. Cerrar sesión")


class Banco:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cuentas = {}

    def registrar_cuenta(self, cuenta):
        self.cuentas[cuenta.numero_cuenta] = cuenta

    def obtener_cuenta(self, numero_cuenta):
        return self.cuentas.get(numero_cuenta)


class Cuenta:
    def __init__(self, numero_cuenta, contraseña, saldo=0, puntos_vive_colombia=0):
        self.numero_cuenta = numero_cuenta
        self.contraseña = contraseña
        self.saldo = saldo
        self.puntos_vive_colombia = puntos_vive_colombia

    def consultar_saldo(self):
        print(f"Saldo actual: ${self.saldo}")

    def realizar_retiro(self):
        valorStr = input("Ingrese el valor a retirar: ")

        if not valorStr.isdigit():
            raise ValueError("El valor ingresado no es válido.")

        valor = float(valorStr)

        if valor < 0:
            raise ValueError("El valor a retirar debe ser mayor a cero.")

        if valor > self.saldo:
            raise RuntimeError("No tiene saldo suficiente para realizar el retiro.")

        if valor > 2000000:
            raise RuntimeError("El valor a retirar supera el límite diario permitido.")

        self.saldo -= valor
        print(f"Retiro exitoso. Nuevo saldo: ${self.saldo}")

    def realizar_transferencia(self, bancos):
        nombreBanco = input("Ingrese el nombre del banco: ")
        numeroCuentaDestino = input("Ingrese el número de cuenta destino: ")
        valorStr = input("Ingrese el valor a transferir: ")

        if not valorStr.isdigit():
            raise ValueError("El valor ingresado no es válido.")

        valor = float(valorStr)

        if valor < 0:
            raise ValueError("El valor a transferir debe ser mayor a cero.")

        bancoDestino = None

        for banco in bancos:
            if banco.nombre.lower() == nombreBanco.lower():
                bancoDestino = banco
                break

        if bancoDestino is None:
            raise ValueError("El nombre del banco no es válido.")

        cuentaDestino = bancoDestino.obtener_cuenta(numeroCuentaDestino)

        if cuentaDestino is None:
            raise ValueError("El número de cuenta destino no es válido.")

        if valor > self.saldo:
            raise RuntimeError("No tiene saldo suficiente para realizar la transferencia.")

        self.saldo -= valor
        cuentaDestino.saldo += valor

        print("Transferencia exitosa.")
        print(f"Nuevo saldo en cuenta origen (${self.numero_cuenta}): ${self.saldo}")
        print(f"Nuevo saldo en cuenta destino (${cuentaDestino.numero_cuenta}): ${cuentaDestino.saldo}")

    def consultar_puntos_vive_colombia(self):
        print(f"Puntos ViveColombia: {self.puntos_vive_colombia}")

    def canjear_puntos_vive_colombia(self):
        puntosStr = input("Ingrese la cantidad de puntos a canjear: ")

        if not puntosStr.isdigit():
            raise ValueError("La cantidad de puntos ingresada no es válida.")

        puntos = int(puntosStr)

        if puntos < 0:
            raise ValueError("La cantidad de puntos a canjear debe ser mayor a cero.")

        valor_canje = puntos / 100

        if valor_canje > self.puntos_vive_colombia:
            raise ValueError("No tiene suficientes puntos para realizar el canje.")

        self.saldo += valor_canje
        self.puntos_vive_colombia -= puntos

        print("Canje de puntos exitoso.")
        print(f"Nuevo saldo: ${self.saldo}")


if __name__ == '__main__':
    bancos = Program.crear_bancos()

    print("Bienvenido al Cajero Automático")

    autenticado = False
    intentos_restantes = 3
    cuenta_autenticada = None

    while not autenticado:
        numero_cuenta = input("Ingrese el número de cuenta: ")
        contraseña = input("Ingrese la contraseña: ")

        cuenta_autenticada = Program.autenticar_cliente(bancos, numero_cuenta, contraseña)

        if cuenta_autenticada is not None:
            autenticado = True
        else:
            intentos_restantes -= 1
            print(f"Número de cuenta o contraseña incorrectos. Intentos restantes: {intentos_restantes}")

            if intentos_restantes == 0:
                print("Ha excedido el número máximo de intentos. Se ha bloqueado la cuenta.")
                exit(0)

    salir = False

    while not salir:
        Program.mostrar_menu()

        opcion_str = input("Seleccione una opción: ")

        if not opcion_str.isdigit():
            print("Opción inválida. Intente nuevamente.")
            continue

        opcion = int(opcion_str)

        print()

        if opcion == 1:
            cuenta_autenticada.consultar_saldo()
        elif opcion == 2:
            try:
                cuenta_autenticada.realizar_retiro()
            except ValueError as ex:
                print(ex)
            except RuntimeError as ex:
                print(ex)
        elif opcion == 3:
            try:
                cuenta_autenticada.realizar_transferencia(bancos)
            except ValueError as ex:
                print(ex)
            except RuntimeError as ex:
                print(ex)
        elif opcion == 4:
            cuenta_autenticada.consultar_puntos_vive_colombia()
        elif opcion == 5:
            try:
                cuenta_autenticada.canjear_puntos_vive_colombia()
            except ValueError as ex:
                print(ex)
        elif opcion == 6:
            salir = True
        else:
            print("Opción inválida. Intente nuevamente.")

        print()

    print("¡Gracias por utilizar el Cajero Automático!")
