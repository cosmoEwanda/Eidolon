# Eidolon — Documentazione delle Classi

## Indice

- [Domain](#domain)
- [Render](#render)
- [Persistence](#persistence)
- [Repository](#repository)
- [Services](#services)
- [UI — Pagine](#ui--pagine)
- [UI — Frame](#ui--frame)
- [UI — Tiles](#ui--tiles)
- [UI — Container](#ui--container)
- [Main](#main)
- [Utils](#utils)

---

## Domain

### CardDefinition (`src/domain/card_definition.py:4`)
Entità principale del dominio che rappresenta una singola carta.
- **Campi**: `id`, `name`, `orders`, `construct`, `rarity`, `ability`, `img`
- **Attributi dinamici**: gestiti tramite `set_attributes(key, value)` / `get_attributes(key)` su un dizionario interno `global_extra_fields`
- **Proprietà**: `to_dict` — serializza la carta in dizionario
- **Costanti di classe**: ereditate da `_card_config` → `VALID_CONSTRUCTS`, `VALID_COSTS`, `VALID_ORDERS`, `VALID_STATS`, `VALID_RARITY`, `VALID_MANA`, `CORE_FIELDS`

### CardFactory (`src/domain/card_factory.py:4`)
Factory statica per creare istanze di `CardDefinition`.
- `from_input(...)` → costruisce da parametri individuali con `extra_attributes` opzionale
- `from_dict(data)` → costruisce da un dizionario, separando i campi core dagli extra

### DeckDefinition (`src/domain/deck_definition.py:3`)
Entità del dominio che rappresenta un mazzo.
- **Campi**: `name`, `cards` (dict `card_id → quantità`), `description`, `avg_cost`, `avg_strenght`
- **Metodi**: `add(card_id)`, `remove(card_id)`, `total_cards()`, `set_avg_cost/set_avg_strenght`, `get_avg_cost/get_avg_strenght`
- **Proprietà**: `to_dict` — serializza il mazzo in dizionario
- **Costanti di classe**: `MAX_COMMON_CARDS=3`, `MAX_RARE_CARDS=2`, `MAX_EPIC_CARDS=1`, `MIN_DECK_CARDS=51`, `MAX_DECK_CARDS=71`

### DeckFactory (`src/domain/deck_factory.py:3`)
Factory statica per creare istanze di `DeckDefinition`.
- `from_dict(data)` → ricostruisce un mazzo da un dizionario (name, cards, description, avg_cost, avg_strenght)

---

## Render

### Padding (`src/render/types.py:4`) — `@dataclass(frozen=True)`
Contenitore immutabile per padding. Campi: `top`, `right`, `bottom`, `left` (default 0).

### Token (`src/render/types.py:12`) — `@dataclass`
Rappresenta un token (testo o icona) in una linea di layout. Campi: `kind` ("text"/"icon"), `value`, `x`, `y`, `font`.

### LayoutResult (`src/render/types.py:20`) — `@dataclass(frozen=True)`
Risultato del calcolo di layout. Campi: `lines` (lista di liste di `Token`), `content_height`.

### TextBoxStyle (`src/render/style.py:5`) — `@dataclass(frozen=True)`
Configurazione di stile per un box di testo.
- **Campi**: `font_path`, `font_size` (default 16), `text_color`, `bg_color`, `icon_size`, `interline` (default 4), `padding` (default `Padding(6,6,6,6)`), `align` ("left"/"right"/"center")

### TextLayout (`src/render/text_layout.py:7`)
Dispone una lista di `Token` in righe entro una larghezza data.
- **Funzionalità**: word-wrapping, dimensionamento icone, calcolo altezza righe, allineamento (left/right/center)
- **Output**: produce un `LayoutResult` con posizioni per ogni token
- **Dipende da**: PIL `ImageDraw` per la misurazione del testo

### TextBoxRenderer (`src/render/text_box_renderer.py:4`)
Renderizza un `LayoutResult` in un'immagine PIL.
- `render(layout, width, style)` → per layout complessi
- `render_simple(text, width, style)` → per testo monoriga
- Usa una `icon_cache` per cercare percorsi delle icone

### AutoFitTextBoxBuilder (`src/render/autofit_text_box_builder.py:6`)
Costruisce box di testo con auto-adattamento del font size.
- Usa `EffectParser` per tokenizzare il testo
- Prova dimensioni decrescenti (da `style.font_size` a `min_font_size=8`) finché il testo entra nell'altezza data
- Delega il rendering al `TextBoxRenderer` iniettato

### EffectParser (`src/render/effect_parser.py:4`)
Parsa il testo abilità di una carta in token.
- Riconosce pattern `[nome_icona]` come token icona
- Divide i segmenti di testo tra le icone in token testo

### RenderCard (`src/render/render_card.py:3`)
Gestisce il rendering composito di una carta su un template.
- Apre un'immagine template (PNG)
- `render_external_image(image_path, posx, posy, dim)` → incolla immagini sul template
- `get_template()` → restituisce l'immagine finale compositata

---

## Persistence

### JsonCardStorage (`src/persistence/json_card_storage.py:5`)
Persistenza su file JSON per le carte.
- Ogni carta salvata come `{card_id}.json` in una cartella
- **Metodi**: `save(card_id, data)`, `delete(card_id)`, `get_by_id(card_id)`, `load_all()`

### JsonDeckStorage (`src/persistence/json_deck_storage.py:7`)
Persistenza su file JSON per i mazzi.
- Ogni mazzo salvato come `{name}.json`
- Usa scritture atomiche (temp file + `os.replace`)
- **Metodi**: `save(name, data)`, `delete(name)`, `load_all()`, `get_by_name(name)`

### GoogleDriveCardStorage (`src/persistence/googleDrive_card_storage.py:6`)
Recupera dati carte da Google Sheets pubblicati come CSV.
- `load_raw()` → legge tre fogli (carte, ordini, costi) via `pd.read_csv()` e restituisce un dict di DataFrame
- Lancia `ConnectionError("NO_INTERNET")` in caso di errore di rete

### CardSheetMapper (`src/persistence/card_sheet_mapper.py:7`)
Mappa i DataFrame di Google Sheets in oggetti `CardDefinition`.
- `map(raw, art_dir)` → elabora ogni riga estraendo ordini, costi, statistiche, sinergie
- Metodi privati: `_extract_sinergy`, `_extract_orders`, `_extract_cost`, `_extract_stats`

---

## Repository

### CardRepository (`src/repository/card_repository.py:3`)
Layer repository che converte `CardDefinition` ↔ dict e delega a `JsonCardStorage`.
- **Metodi**: `save_card(card)`, `delete_card(cid)`, `get_all_cards()`, `get_card_by_id(cid)`, `exists(cid)`

### DeckRepository (`src/repository/deck_repository.py:3`)
Layer repository che converte `DeckDefinition` ↔ dict e delega a `JsonDeckStorage`.
- **Metodi**: `save_deck(deck)`, `get_all_decks()`, `get_deck_by_name(name)`, `delete_deck(name)`, `exists(name)`

---

## Services

### CardBasicService (`src/services/card_basic_service.py:4`)
Logica di business per le carte.
- Calcola e attacca hash ai dati carta
- **Metodi**: `save_card_service(card)`, `delete_card_service(card_id)`, `get_all_cards_service()`, `get_card_by_id_service(card_id)`, `get_hash_map()`, `sync_cards(remote_cards)` (riconciliazione create/update/delete tra remoto e locale)

### DeckBasicService (`src/services/deck_basic_service.py:3`)
Logica di business per i mazzi.
- Impone nomi univoci (lancia `DeckNameAlreadyExistsError` se il nome esiste già)
- **Metodi**: `create_deck_service(deck)`, `update_deck_service(deck)`, `delete_deck_service(deck_name)`, `get_all_decks_service()`

### CardRendererService (`src/services/card_renderer_service.py:5`)
Orchestratore di rendering carte di alto livello.
- Prende: libreria assets, dizionario layout (configurazioni di rendering), text builder/renderer, directory immagini
- `render_and_save(card, out_path)` → seleziona layout per construct della carta, compone template, elementi di testo, icone ordini e artwork

### CardLoader (`src/services/card_loader.py:1`)
Orchestratore del pipeline di sincronizzazione completo.
- Collega: `GoogleDriveCardStorage` → `CardSheetMapper` → `CardBasicService.sync_cards` → `ImageRenderSync.sync`
- **Metodi**: `sync_remote_to_local(art_dir)`, `clean_catalog()`, `load_image_by_id(card_id)`, `update_image_catalog()`

### DeckStatistics (`src/services/deck_statistics.py:1`)
Calcola statistiche per un mazzo.
- Costruttore carica tutte le carte via `card_service` e le cache
- **Metodi**: `calculate_avg_cost(target_cost)`, `calculate_avg_strenght(target_strenght)`, `get_Ncards()`

### DeckPrintService (`src/services/deck_print_service.py:18`)
Genera un PDF delle carte di un mazzo con `reportlab`.
- Griglia configurabile (righe/colonne)
- Supporta anteprima (apre il PDF nel visualizzatore predefinito) e stampa via `os.startfile`
- Gestione atomica del PDF, cache immagini, adattamento immagini alle celle
- **Metodi**: `build_grid_preview(deck, title, n_cards_per_row, n_cards_per_col)` e interno `_build_grid`

### ImageRenderSync (`src/services/image_render_sync.py:9`)
Sincronizza le immagini renderizzate su disco.
- Confronta hash JSON con metadati salvati (`_render_meta.json`) per determinare quali carte necessitano re-rendering
- Usa `ThreadPoolExecutor` per rendering parallelo
- Gestisce pulizia orfani PNG e scrittura atomica metadati
- **Metodi**: `sync(cards, force=False)`

---

## UI — Container

### DeckWindowContainer (`src/ui/deck_windows_container.py:7`) — `Frame`
Navigatore di pagine (router) dell'interfaccia.
- Gestisce la navigazione tra `DecksPage`, `DeckDetailPage` e `DeckBuilderPage`
- Crea `DeckPrintService` per la generazione PDF
- **Callback**: `open_deck`, `new_deck`, `_save_new_deck`, `_after_delete_deck`, `_edit_deck`, `_save_edited_deck`, `_print_preview_deck`

---

## UI — Pagine

### DecksPage (`src/ui/pages/decks_page.py:6`) — `Frame`
Pagina home/galleria che mostra tutti i mazzi esistenti.
- Griglia di `DeckTile` (fino a 6 per riga, max 35 mazzi)
- Include `NewDeckTile` per creare nuovi mazzi
- **Metodi**: `reload()` — aggiorna la visualizzazione

### DeckDetailPage (`src/ui/pages/deck_detail_page.py:5`) — `Frame`
Mostra i dettagli di un mazzo selezionato.
- Nome, descrizione, lista carte (via `CardSheetMakerFrame`), statistiche (conteggio carte, costo medio, forza media)
- Pulsanti: anteprima stampa, elimina mazzo, modifica mazzo, pubblica PDF su Google Drive

### DeckBuilderPage (`src/ui/pages/deck_builder_page.py:8`) — `Frame`
Editor di mazzi.
- Sinistra: `CardCatalogFrame` per sfogliare/cercare carte
- Destra: `DeckListFrame` con la composizione corrente del mazzo
- Supporta: aggiunta carte via doppio click, modifica mazzi esistenti, visualizzazione immagini, ricaricamento arte selezionata, salvataggio (calcola statistiche prima del salvataggio via `DeckStatistics`)

---

## UI — Frame

### CardCatalogFrame (`src/ui/frames/card_catalog_frame.py:5`) — `Frame`
Involucro che contiene `CardSheetMakerFrame` e aggiunge menu contestuale.
- Doppio click → aggiunge carta al mazzo
- Click destro → visualizza carta
- Pulsanti: toggle segnalini ricarica, ricarica arte segnata, cancella segnalini

### CardImageWindow (`src/ui/frames/card_image_window.py:5`) — `Toplevel`
Finestra popup che mostra l'immagine di una carta con tracciamento mouse.
- Mostra coordinate originali vs layout mentre il mouse si muove sull'immagine
- Utile per debug del layout

### CardSheetMakerFrame (`src/ui/frames/cardsheet_maker_frame.py:7`) — `Frame`
Widget `Treeview` scrollabile che mostra un catalogo di carte.
- Raggruppa per ID carta, mostra quantità
- Colonne configurabili definite in `_cardsheet_config.COLUMNS_MAP`
- Funzionalità: checkbox "ricarica arte" cliccabile, tooltip su hover per testo troncato

### DeckListFrame (`src/ui/frames/deck_list_frame.py:3`) — `Frame`
Mostra il mazzo corrente in modifica.
- Campo nome mazzo, lista carte con pulsanti `+`/`-` per quantità
- Area scrollabile con supporto rotellina mouse
- Conteggio totale carte, pulsante Salva
- **Metodi**: `refresh()`, `selected_cards()`, `deck_name()`

---

## UI — Tiles

### DeckTile (`src/ui/tiles/deck_tile.py:4`) — `Frame`
Pulsante tile cliccabile (70x70) che rappresenta un mazzo esistente.
- Mostra il nome del mazzo (wrapped)
- Al click chiama il callback `command` iniettato

### NewDeckTile (`src/ui/tiles/new_deck_tile.py:4`) — `Frame`
Tile evidenziato in verde (`"+\nNuovo"`) per creare un nuovo mazzo.
- Stesse dimensioni di `DeckTile` (70x70)

---

## Main

### MainUI (`src/main_ui.py:92`) — `Tk`
Finestra principale dell'applicazione.
- Inizializza tutta l'infrastruttura: storage JSON/Google Drive, repository, servizi, renderer, loader
- Crea i pulsanti "Aggiorna catalogo" e "Cancella catalogo"
- Crea il mazzo rune all'avvio
- All'avvio esegue `check_update()` che interroga GitHub Releases per aggiornamenti automatici
- **Entry point**: se eseguito direttamente → `check_update()` → `MainUI()` → `mainloop()`

---

## Utils

### DeckNameAlreadyExistsError (`src/utils/errors.py:1`) — `Exception`
Eccezione personalizzata lanciata quando si tenta di creare un mazzo con un nome già esistente.

### PdfInUseError (`src/services/deck_print_service.py:13`) — `RuntimeError`
Eccezione lanciata quando il file PDF non può essere sovrascritto (probabilmente aperto in un visualizzatore).
