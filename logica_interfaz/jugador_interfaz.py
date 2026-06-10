from logica_interfaz.archivo_de_importaciones import importar_desde_carpeta

Jugador = importar_desde_carpeta(
    "jugador.py", #Archivo
    "Jugador" #Clase
    )

Elemento_texto = importar_desde_carpeta(
    "elementos_de_interfaz_de_usuario.py", #Archivo
    "Elemento_texto", #Clase
    "recursos_graficos" #Nombre de la carpeta
    )

constantes = importar_desde_carpeta(
    nombre_archivo="constantes.py",
    nombre_carpeta="recursos_graficos"
    )

class Jugador_interfaz(Jugador):
    def __init__(self,*args,un_juego=None,x=0,y=0,ancho=0,alto=0,**kwargs):
        self.un_juego = un_juego
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        super().__init__(*args,**kwargs)
#cambio lismar
    def elemento_usuario(self, mostrar_nombre=True, es_turno=False):
        nombre_corto = self.nombre_jugador
        if len(nombre_corto) > 12:
            nombre_corto = nombre_corto[:10] + "..."
            
        usuario = PanelJugadorVisual(self.un_juego, nombre_corto, self.x, self.y, self.nro_jugador)
        
        if es_turno:
            usuario.color_borde_actual = constantes.NARANJA
        else:
            usuario.color_borde_actual = usuario.color_dorado
            
        # <── EL CABLE DIRECTO: Guardamos el panel visual dentro de la memoria del jugador
        self.mi_panel_visual = usuario 
        
        return usuario


class PanelJugadorVisual:
    """Clase personalizada que dibuja la credencial de jugador a escala ÓPTIMA"""
    def __init__(self, un_juego, nombre, x, y, id_jugador):
        import pygame
        self.pantalla = un_juego.pantalla
        self.nombre = nombre
        self.cartas = 0
        self.puntos = 0
        self.x = x
        self.y = y
        self.id_jugador = id_jugador
        self.visible = True
        self.rect = pygame.Rect(x, y, 100, 100) 
        
        self.color_vino = (65, 25, 30)       
        self.color_dorado = (194, 155, 87)   
        self.blanco = (255, 255, 255)
        self.color_borde_actual = self.color_dorado
        
        # Fuentes de tamaño intermedio
        try:
            self.fuente_nombre = pygame.font.Font(constantes.FUENTE_ESTANDAR, 28)
            self.fuente_cartas_lbl = pygame.font.Font(constantes.FUENTE_ESTANDAR, 14)
            self.fuente_numero = pygame.font.Font(constantes.FUENTE_ESTANDAR, 24)
            self.fuente_pts = pygame.font.Font(constantes.FUENTE_ESTANDAR, 30)
        except:
            import pygame.font
            self.fuente_nombre = pygame.font.SysFont("arial", 28, bold=True)
            self.fuente_cartas_lbl = pygame.font.SysFont("arial", 14, bold=True)
            self.fuente_numero = pygame.font.SysFont("arial", 24, bold=True)
            self.fuente_pts = pygame.font.SysFont("arial", 30, bold=True)

    def dibujar(self):
        if not self.visible: return
        import pygame
        
        txt_nombre = self.fuente_nombre.render(self.nombre, True, self.blanco)
        txt_lbl_cartas = self.fuente_cartas_lbl.render("cartas", True, self.blanco)
        txt_num_cartas = self.fuente_numero.render(str(self.cartas), True, self.color_vino)
        
        ancho_pastilla = max(txt_num_cartas.get_width() + 20, 45)
        alto_pastilla = txt_num_cartas.get_height() + 6
        
        margen = 15
        espacio_medio = 20
        ancho_top = margen + txt_nombre.get_width() + espacio_medio + max(txt_lbl_cartas.get_width(), ancho_pastilla) + margen
        alto_top = 58 
        
        txt_pts_lbl = self.fuente_pts.render("Pts: ", True, self.blanco)
        txt_pts_num = self.fuente_pts.render(str(self.puntos), True, self.color_dorado)
        
        ancho_bottom = margen + txt_pts_lbl.get_width() + txt_pts_num.get_width() + margen
        alto_bottom = 48 
        
        rect_top = pygame.Rect(self.x, self.y, ancho_top, alto_top)
        pygame.draw.rect(self.pantalla, self.color_vino, rect_top, border_radius=10)
        pygame.draw.rect(self.pantalla, self.color_borde_actual, rect_top, width=3, border_radius=10)
        
        y_centro_top = self.y + (alto_top // 2)
        self.pantalla.blit(txt_nombre, (self.x + margen, y_centro_top - (txt_nombre.get_height() // 2)))
        
        x_zona_cartas = self.x + ancho_top - margen - ancho_pastilla
        self.pantalla.blit(txt_lbl_cartas, (x_zona_cartas + (ancho_pastilla - txt_lbl_cartas.get_width()) // 2, self.y + 4))
        
        rect_pastilla = pygame.Rect(x_zona_cartas, self.y + 24, ancho_pastilla, alto_pastilla)
        pygame.draw.rect(self.pantalla, self.blanco, rect_pastilla, border_radius=10)
        self.pantalla.blit(txt_num_cartas, (rect_pastilla.centerx - (txt_num_cartas.get_width() // 2), rect_pastilla.centery - (txt_num_cartas.get_height() // 2)))
        
        offset_x = margen + (txt_nombre.get_width() * 0.3)
        rect_bottom = pygame.Rect(self.x + offset_x, self.y + alto_top - 4, ancho_bottom, alto_bottom)
        
        pygame.draw.rect(self.pantalla, self.color_vino, rect_bottom, border_radius=10)
        pygame.draw.rect(self.pantalla, self.color_borde_actual, rect_bottom, width=3, border_radius=10)
        
        x_pts = rect_bottom.x + margen
        y_pts = rect_bottom.y + (alto_bottom - txt_pts_lbl.get_height()) // 2
        self.pantalla.blit(txt_pts_lbl, (x_pts, y_pts))
        self.pantalla.blit(txt_pts_num, (x_pts + txt_pts_lbl.get_width(), y_pts))
        
        self.rect = pygame.Rect(self.x, self.y, max(ancho_top, offset_x + ancho_bottom), alto_top + alto_bottom - 4)

    def manejar_evento(self, evento):
        return False

    def verificar_hover(self, posicion_raton):
        return False