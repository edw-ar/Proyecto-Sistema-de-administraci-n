import flet as ft
from src.logic.validaciones import es_numero, es_entero, es_fecha

class Formulario(ft.Column):
    def __init__(self, on_guardar_callback):
        super().__init__()
        self.on_guardar = on_guardar_callback

        self.campos_opc = {
            "lote": ft.TextField(label="Lote", hint_text="Ej: L0001"),
            "codigo": ft.TextField(label="Código", hint_text="Ej: 5263GS3"),
            "precio": ft.TextField(label="Precio", hint_text="Ej: 34.50", keyboard_type=ft.KeyboardType.NUMBER),
            "unidad": ft.Dropdown(
                        label="Unidad",
                        width=180,
                        value="lote",
                        options=[
                            ft.dropdown.Option(key="Blister", text="Blister"),
                            ft.dropdown.Option(key="Frasco",  text="Frasco"),
                            ft.dropdown.Option(key="Botella", text="Botella"),
                            ft.dropdown.Option(key="Caja_Paquete", text="Caja/Paquete"),
                            ft.dropdown.Option(key="Otro", text="Otro"),
                        ],
                    ),
            "cantidad": ft.TextField(label="Cantidad", hint_text="Ej: 36", keyboard_type=ft.KeyboardType.NUMBER),
            "tipo": ft.Dropdown(
                        label="Tipo de producto",
                        width=180,
                        value="lote",
                        options=[
                            ft.dropdown.Option(key="Analgesicos_y_antipireticos", text="Analgésicos o antipireticos"),
                            ft.dropdown.Option(key="Antiinflamatorios", text="Antiinflamatorios"),
                            ft.dropdown.Option(key="Antibioticos_antibacterianos", text="Antibióticos/Antibacterianos"),
                            ft.dropdown.Option(key="Antivirales", text="Antivirales"),
                            ft.dropdown.Option(key="Antialergicos", text="Antialérgicos"),
                            ft.dropdown.Option(key="Antiacidos_y_protectores_gastricos", text="Antiácidos o protectores gastricos"),
                            ft.dropdown.Option(key="Antidiarreicos_y_laxantes", text="Antidiarreicos o laxantes"),
                            ft.dropdown.Option(key="Psicotropicos_y_ansioliticos", text="Psicotrópicos o ansiolíticos")
                        ],
                    ),
            "fech_entr": ft.TextField(label="Fecha entrada", hint_text="DD/MM/AAAA"),
            "fech_venc": ft.TextField(label="Fecha vencimiento", hint_text="DD/MM/AAAA"),
        }
        self.lista_campos = list(self.campos_opc.values())
        self.mensaje = ft.Text("", size=13)

        filas = []
        lista_keys = list(self.campos_opc.keys())
        for i in range(0, len(lista_keys), 2):
            filas.append(self.crear_fila(lista_keys[i], lista_keys[i+1] if i+1 < len(lista_keys) else None))

        self.controls = [
            ft.Text("➕ Agregar Producto", size=24, weight="bold"),
            *filas,
            ft.Button("Guardar", on_click=self.on_click_guardar, bgcolor='#2E4957', color="white"),
            self.mensaje
            ]

    def crear_fila(self, k1, k2):
        c1 = self.campos_opc[k1]
        c1.expand = True
        if k2:
            c2 = self.campos_opc[k2]
            c2.expand = True
            return ft.Row([c1, c2], spacing=20)
        return ft.Row([c1], spacing=20)
        
    def marcar_error(self, campo, texto):
        campo.error_text = texto
        campo.border_color = ft.Colors.RED_600
        campo.value = ""
            
    def validar(self):
        valido = True
        for c in self.lista_campos:
            c.error_text = None
            c.border_color = None
            if not c.value or str(c.value).strip() == "":
                self.marcar_error(c, "Obligatorio")
                valido = False
        
        if self.campos_opc["precio"].error_text is None and not es_numero(self.campos_opc["precio"].value):
            self.marcar_error(self.campos_opc["precio"], "Debe ser número"); valido = False
        if self.campos_opc["cantidad"].error_text is None and not es_entero(self.campos_opc["cantidad"].value):
            self.marcar_error(self.campos_opc["cantidad"], "Debe ser entero"); valido = False
        for k in ["fech_entr", "fech_venc"]:
            if self.campos_opc[k].error_text is None and not es_fecha(self.campos_opc[k].value):
                self.marcar_error(self.campos_opc[k], "Formato: DD/MM/AAAA"); valido = False
        
        self.update()
        return valido

    def on_click_guardar(self, e):
        if self.validar():
            datos = {k: v.value.strip() for k, v in self.campos_opc.items()}
            self.on_guardar(datos, self)
        else:
            self.mensaje.value = "⚠ Corrige los campos marcados."
            self.mensaje.color = ft.Colors.RED_600
            self.update()

    def limpiar(self):
        for c in self.lista_campos:
            c.value = ""; c.error_text = None; c.border_color = None
        self.update()