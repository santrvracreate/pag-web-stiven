"""Regenera las cuatro páginas estáticas. Sin dependencias de ejecución."""
from pathlib import Path
import json
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT/'docentes.js').read_text(encoding='utf-8')
data = json.loads(raw.split('window.schoolStaff = ',1)[1].rstrip(';\n'))
areas = {a['id']:a['name'] for a in data['areas']}

def icon(name):
    paths={
      'arrow':'<path d="M5 12h14m-6-6 6 6-6 6"/>',
      'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',
      'book':'<path d="M12 5v15M3 4c4-1 6 0 9 2 3-2 5-3 9-2v15c-4-1-6 0-9 2-3-2-5-3-9-2Z"/>',
      'music':'<path d="M9 17V5l11-2v12M9 9l11-2"/><ellipse cx="6" cy="18" rx="3" ry="2"/><ellipse cx="17" cy="16" rx="3" ry="2"/>',
      'flag':'<path d="M5 21V3m0 1c5-4 9 4 15 0v10c-6 4-10-4-15 0"/>',
      'expand':'<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
      'left':'<path d="m14 5-7 7 7 7"/>',
      'right':'<path d="m10 5 7 7-7 7"/>',
      'close':'<path d="m6 6 12 12M6 18 18 6"/>'
    }
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[name]+'</svg>'

def image(src,alt,cls='',lazy=True,width=800,height=600):
    return f'<img src="{quote(src,safe="/")}" alt="{escape(alt)}" class="{cls}" width="{width}" height="{height}" loading="{"lazy" if lazy else "eager"}" decoding="async">'

def header(active):
    nav=''.join(f'<a href="{file}.html"'+(' aria-current="page"' if file==active else '')+f'>{label}</a>' for file,label in [('index','Inicio'),('profesores','Plantel Docente'),('banda','Banda'),('escoltas','Escoltas')])
    return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a>
    <div class="topline"><div class="container"><span>Educación que nos une.</span><span>Sacaba, Cochabamba · Bolivia</span></div></div>
    <header class="site-header"><div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Unidad Educativa José Leoncio Capriles — Inicio">{image('logos/logo.jpg','Escudo de la Unidad Educativa José Leoncio Capriles',lazy=False,width=206,height=206)}<span><small>UNIDAD EDUCATIVA</small><strong>José Leoncio Capriles</strong></span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="Abrir menú"><span></span><span></span><span></span></button>
    <nav id="navigation" aria-label="Navegación principal">{nav}</nav></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="container footer-inner"><div class="footer-brand">{image('logos/logo.jpg','Escudo institucional',width=206,height=206)}<div><strong>Unidad Educativa José Leoncio Capriles</strong><p>Sacaba, Cochabamba, Bolivia.</p></div></div><p class="copyright">© <span data-year>2026</span> · Todos los derechos reservados.</p></div></footer>'''

def page(file,title,description,body):
    html=f'''<!DOCTYPE html>
<html lang="es-BO"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#D2141C"><meta name="description" content="{description}"><title>{title} | U. E. José Leoncio Capriles</title><link rel="icon" href="logos/logo.jpg"><link rel="stylesheet" href="styles.css">{'<script src="docentes.js" defer></script>' if file=='profesores' else ''}<script src="script.js" defer></script></head>
<body data-page="{file}">{header(file)}<main id="contenido">{body}</main>{footer()}</body></html>'''
    (ROOT/f'{file}.html').write_text(html,encoding='utf-8')

def home():
    cards=''
    for file,title,desc,src,alt,ico in [
      ('profesores','Plantel Docente','Las personas que acompañan cada aprendizaje.','profesores/lenguaje/Edva Garisto Valencia.png','Prof. Edva Garisto Valencia','book'),
      ('banda','Banda Estudiantil','El talento que da ritmo a nuestra identidad.','banda/img4.jpg','Banda estudiantil reunida en el patio','music'),
      ('escoltas','Nuestros Escoltas','Compromiso y respeto por nuestros símbolos.','escoltas/img1.jpg','Escoltas en una actividad institucional','flag')]:
        cards+=f'''<a class="explore-card" href="{file}.html"><div class="card-photo">{image(src,alt)}<span class="card-icon">{icon(ico)}</span></div><div class="card-content"><h3>{title}</h3><p>{desc}</p><span class="text-link">Conocer más {icon('arrow')}</span></div></a>'''
    return f'''<section class="hero container" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">UNIDAD EDUCATIVA</p><h1 id="hero-title">José Leoncio<br><span>Capriles</span></h1><p class="hero-location"><span class="gold-rule"></span>Sacaba, Cochabamba — Bolivia</p><p class="hero-description">Una comunidad que aprende, crece y comparte. Bienvenidos a un espacio donde la educación, el talento y los valores nos unen.</p><a class="button" href="profesores.html">Conocer nuestro plantel {icon('arrow')}</a></div>
    <div class="hero-visual"><div class="hero-photo">{image('banda/img3.jpg','Nuestra banda estudiantil reunida en la Unidad Educativa José Leoncio Capriles',lazy=False,width=1600,height=1109)}</div><div class="hero-seal">{image('logos/logo.jpg','Escudo oficial',lazy=False,width=206,height=206)}<div><span>NUESTRA IDENTIDAD</span><strong>Orgullo de ser Capriles.</strong></div></div><span class="photo-note">Nuestra comunidad educativa</span></div></section>
    {history()}
    <section class="community"><div class="container"><div class="section-heading"><div><p class="eyebrow">VIDA INSTITUCIONAL</p><h2>Una comunidad, muchas formas de crecer.</h2></div><p>Conoce a quienes dan vida<br>a nuestra institución.</p></div><div class="explore-grid">{cards}</div></div></section>'''

def history():
    return f'''<section class="history-section container" aria-labelledby="history-title">
    <div class="history-heading"><p class="eyebrow">NUESTRA HISTORIA</p><h2 id="history-title">Una historia que nos une a Sacaba.</h2><p class="history-lead">Educación, memoria y comunidad.</p><figure class="history-photo">{image('banda/img3.jpg','La comunidad estudiantil frente al edificio de la institución',width=1600,height=1109)}<figcaption>La institución y su comunidad educativa.</figcaption></figure></div>
    <div class="history-copy">
    <p>La Unidad Educativa José Leoncio Capriles forma parte de la vida educativa de Sacaba, Cochabamba. El programa conmemorativo de sus Bodas de Oro recoge el período <strong>1973–2023</strong> como referencia de su trayectoria institucional: una memoria compartida por docentes, estudiantes, familias y exalumnos. <a class="source-mark" href="#history-source-1" aria-label="Consultar fuente del programa de Bodas de Oro">[1]</a></p>
    <p>Entre los hitos documentados de su crecimiento se encuentra la entrega de una nueva infraestructura en <strong>2016</strong>. La nota publicada por el diario Opinión describe un edificio de tres plantas, con nueve aulas, laboratorios de química y salas de computación. Esta ampliación incorporó espacios destinados al aprendizaje y a las actividades académicas del colegio. <a class="source-mark" href="#history-source-2" aria-label="Consultar fuente sobre la infraestructura de 2016">[2]</a></p>
    <p>El programa de las <strong>Bodas de Oro de 2023</strong> contempló actividades cívicas, religiosas, artísticas y deportivas durante marzo, además de una jornada dedicada al exalumno. En su organización figuraban la dirección, el plantel docente y administrativo, los estudiantes y los padres de familia, reflejando el carácter comunitario de la conmemoración. <a class="source-mark" href="#history-source-1" aria-label="Consultar fuente de las actividades conmemorativas">[1]</a></p>
    <p>Hoy, la presentación de su plantel docente, su banda estudiantil y sus escoltas permite conocer distintas expresiones de esa comunidad. La enseñanza, la música y la participación institucional forman parte de la identidad que el colegio comparte desde Sacaba.</p>
    <div class="history-sources" aria-label="Fuentes de la reseña histórica"><span>Fuentes de la reseña</span><a id="history-source-1" href="https://es.scribd.com/document/630250100/CRONOGRAMA-BODAS-DE-ORO-1973-2023" target="_blank" rel="noopener noreferrer">1. Programa de Bodas de Oro 1973–2023 · copia pública en Scribd</a><a id="history-source-2" href="https://www.opinion.com.bo/cochabamba/sacaba-entrega-obras-cerca-aniversario/20160626200100553736.html" target="_blank" rel="noopener noreferrer">2. Diario Opinión · 26 de junio de 2016</a></div>
    </div></section>'''

def teacher_card(t):
    portrait=image(t['photo'],'Prof. '+t['name'],width=400,height=400) if t['photo'] else f'<div class="initials" role="img" aria-label="Iniciales de {escape(t["name"])}"><span>MR</span></div>'
    paragraphs = ''.join('<p>'+escape(p)+'</p>' for p in t['bio'].split('\n\n') if p.strip())
    return f'''<article class="teacher-card" id="{t['id']}"><div class="teacher-photo">{portrait}</div><div class="teacher-copy"><p class="specialty">{' · '.join(areas[a] for a in t['areas'])}</p><h3><span>Prof.</span> {escape(t['name'])}</h3><div class="teacher-bio">{paragraphs}</div></div></article>'''

def teachers():
    chips='<button class="area-button active" data-area="all" aria-pressed="true">Todas las áreas</button>'+''.join(f'<button class="area-button" data-area="{a["id"]}" aria-pressed="false">{a["name"]}</button>' for a in data['areas'])
    groups=''
    for a in data['areas']:
        cards=''.join(teacher_card(t) for t in data['teachers'] if t['areas'][0]==a['id'])
        cross='<p class="shared-specialty">También forma parte de esta área: <a href="#mariela-orellana-jaldin">Prof. Mariela Orellana Jaldín · Física y Química</a>.</p>' if a['id']=='quimica' else ''
        groups+=f'<section class="subject-group" data-group="{a["id"]}" aria-labelledby="area-{a["id"]}"><h2 id="area-{a["id"]}">{a["name"]}</h2>{cards}{cross}</section>'
    return f'''<section class="page-intro container"><p class="eyebrow">PERSONAS QUE INSPIRAN</p><h1>Nuestro plantel docente</h1><p>Compromiso con la enseñanza. Vocación para acompañar.</p></section>
    <section class="director container" aria-labelledby="director-name"><div class="director-photo">{image('dire/wilson mercado flores.PNG','Wilson Mercado Flores, director',lazy=False,width=300,height=329)}</div><div class="director-copy"><p class="eyebrow">DIRECCIÓN</p><h2 id="director-name">Wilson Mercado Flores</h2><p class="director-role">Director</p><div class="director-signature"><span class="gold-rule"></span>Unidad Educativa José Leoncio Capriles</div></div></section>
    <section class="staff-section container" aria-labelledby="staff-title"><div class="staff-heading"><div><p class="eyebrow">NUESTROS EDUCADORES</p><h2 id="staff-title">El valor de enseñar.</h2></div><div class="search-field"><label class="sr-only" for="teacher-search">Buscar docente por nombre o asignatura</label>{icon('search')}<input id="teacher-search" type="search" placeholder="Buscar por nombre o asignatura" autocomplete="off"></div></div>
    <div class="staff-layout"><aside class="areas"><p class="filter-title">EXPLORAR POR ÁREA</p><div class="area-options" aria-label="Filtrar por asignatura">{chips}</div></aside><div class="staff-results"><p id="results-status" class="results-status" role="status" aria-live="polite">Todas las áreas del plantel</p><div id="teacher-groups">{groups}</div><div class="empty-state" hidden><h3>No encontramos coincidencias.</h3><p>Prueba con otro nombre o asignatura.</p><button class="button" id="reset-search">Ver todo el plantel {icon('arrow')}</button></div></div></div></section>'''

GALLERIES={
 'banda': [('banda/img3.jpg','Integrantes de la banda estudiantil reunidos frente al edificio de la institución',1600,1109),('banda/img4.jpg','Banda estudiantil en el patio cubierto de la institución',2048,1536),('banda/img5.jpg','Integrantes de la banda con sus instrumentos en el patio',2048,1536),('banda/img1.jfif','Participantes junto a la banda durante una actividad institucional',646,475),('banda/img2.jfif','Banda estudiantil reunida en el espacio deportivo cubierto',516,387)],
 'escoltas': [('escoltas/img1.jpg','Escoltas en formación en el patio de la institución',2048,1536),('escoltas/img2.jfif','Escoltas participando en una actividad institucional',673,456),('escoltas/img3.jfif','Escoltas con banderas durante una actividad al aire libre',396,774)]
}

def photo_button(item,cls='',eager=False):
    src,alt,w,h=item
    return f'<button class="gallery-photo {cls}" data-full="{quote(src,safe="/")}" aria-label="Ampliar: {escape(alt)}">{image(src,alt,lazy=not eager,width=w,height=h)}<span class="expand-icon">{icon("expand")}</span></button>'

def gallery(which):
    is_band=which=='banda'
    title='Nuestra Banda Estudiantil' if is_band else 'Nuestros Escoltas'
    subtitle='Talento, disciplina y orgullo institucional.' if is_band else 'Compromiso, responsabilidad y orgullo institucional.'
    intro='La música reúne a nuestra comunidad. La banda estudiantil es un espacio para compartir el talento, cultivar la disciplina y vivir el trabajo en equipo a través de cada interpretación.' if is_band else 'El respeto por nuestros símbolos se expresa en cada formación. Nuestros escoltas representan el compromiso, la responsabilidad y el sentido de pertenencia a la comunidad educativa.'
    items=GALLERIES[which]
    if is_band:
        slides=''.join(f'<div class="slide"'+(' hidden' if i else '')+'>'+photo_button(item,'slide-photo',eager=i==0)+'</div>' for i,item in enumerate(items))
        dots=''.join(f'<button class="carousel-dot{" active" if i==0 else ""}" aria-label="Mostrar vista {i+1} de la banda" aria-pressed="{"true" if i==0 else "false"}" data-slide="{i}"></button>' for i in range(len(items)))
        photos=f'''<section class="carousel" aria-label="Fotografías de la banda estudiantil" aria-roledescription="carrusel"><div class="slides">{slides}</div><div class="carousel-bar"><span>Banda Estudiantil · José Leoncio Capriles</span><div class="carousel-controls"><button class="icon-button" data-direction="-1" aria-label="Fotografía anterior">{icon('left')}</button><div class="carousel-dots">{dots}</div><button class="icon-button" data-direction="1" aria-label="Fotografía siguiente">{icon('right')}</button></div></div><span class="sr-only" id="carousel-status" role="status" aria-live="polite"></span></section>
        <section class="gallery-section" aria-labelledby="gallery-title"><div class="gallery-heading"><h2 id="gallery-title">La música nos reúne.</h2><p>Instantes de nuestra banda estudiantil.</p></div><div class="photo-grid band-grid">{''.join(photo_button(item) for item in items[1:])}</div></section>'''
    else:
        photos=f'''<section class="escort-gallery" aria-label="Galería de escoltas">{photo_button(items[0],'escort-main',eager=True)}<div class="escort-pair">{photo_button(items[1])}{photo_button(items[2],'portrait')}</div></section>'''
    modal=f'''<dialog class="lightbox" aria-label="Fotografía ampliada"><button class="lightbox-close icon-button" aria-label="Cerrar visor">{icon('close')}</button><button class="lightbox-prev icon-button" aria-label="Fotografía anterior">{icon('left')}</button><img class="lightbox-image" alt=""><button class="lightbox-next icon-button" aria-label="Fotografía siguiente">{icon('right')}</button><p class="sr-only" id="lightbox-status" role="status"></p></dialog>'''
    return f'''<section class="page-intro container gallery-intro"><p class="eyebrow">VIDA INSTITUCIONAL</p><h1>{title}</h1><p>{subtitle}</p><div class="intro-rule"></div></section><div class="container gallery-content"><p class="gallery-description">{intro}</p>{photos}</div>{modal}'''

page('index','Inicio','Conoce la Unidad Educativa José Leoncio Capriles de Sacaba, Cochabamba: nuestro plantel docente, banda estudiantil y escoltas.',home())
page('profesores','Plantel Docente','Conoce al director y al plantel docente de la Unidad Educativa José Leoncio Capriles, organizado por asignatura.',teachers())
page('banda','Banda Estudiantil','Talento, disciplina y orgullo institucional. Fotografías de nuestra banda estudiantil.',gallery('banda'))
page('escoltas','Nuestros Escoltas','Compromiso, responsabilidad y orgullo institucional. Galería de nuestros escoltas.',gallery('escoltas'))
print('Cuatro páginas HTML generadas.')
