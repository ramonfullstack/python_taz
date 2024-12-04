from enum import Enum

MAGAZINE_LUIZA_SELLER_ID = 'magazineluiza'

MAGAZINE_LUIZA_SELLER_DESCRIPTION = 'Magalu'

MAGAZINE_LUIZA_DEFAULT_CATEGORY = 'ML'

DEFAULT_CAMPAIGN_CODE = '0'

APPROXIMATE_RECEIVE_COUNT = 'ApproximateReceiveCount'

STAMP_ORIGIN = 'taz.consumers.stamp.consumer'
REBUILD_ORIGIN = 'taz.consumers.rebuild.consumer'
PRODUCT_ORIGIN = 'taz.consumers.product.consumer'
ENRICHED_PRODUCT_ORIGIN = 'taz.consumers.enriched_product.consumer'
PRICE_RULE_ORIGIN = 'taz.consumers.price_rule.consumer'

SINGLE_SELLER_STRATEGY = 'SINGLE_SELLER'
AUTO_BUYBOX_STRATEGY = 'AUTO_BUYBOX'
OMNILOGIC_STRATEGY = 'OMNILOGIC'
CHESTER_STRATEGY = 'CHESTER'

MEDIA_TYPES = ('audios', 'videos', 'podcasts', 'images')

FIRST_FIVE_DIGITS = slice(0, 5, None)

BADGE_CACHE_KEY = 'badge_sku_{sku}_seller_{seller_id}'
INTEGRACOMMERCE_TOKEN_KEY = 'integracommerce_token'
HELENA_TOKEN_KEY = 'helena_token'

META_TYPE_PRODUCT_CLICKS_QUANTITY = 'clicks_quantity'
META_TYPE_PRODUCT_AVERAGE_RATING = 'product_average_rating'
META_TYPE_PRODUCT_TOTAL_REVIEW_COUNT = 'product_total_review_count'
META_TYPE_PRODUCT_SOLD_QUANTITY = 'sold_quantity'

META_TYPE_PRODUCT_IMAGE_SCORE = 'image'
META_TYPE_PRODUCT_FACTSHEET_SCORE = 'factsheet'
PRODUCT_PRESENTATION = 'Apresentação do produto'

DELETE_ACTION = 'delete'
UPDATE_ACTION = 'update'
CREATE_ACTION = 'create'

LEGACY_PRODUCT_ID_LENGTH = 7

DEFAULT_ENTITY = 'Entidade para Filtros Gerais'

ENTITY_TYPE = 'EDDIE_V1'

STOCK_TYPE_DC = 'DC'
STOCK_TYPE_STORE = 'STORE'
STOCK_TYPE_OTHER = 'OTHER'

STOCK_TYPES = {
    'distribution center': STOCK_TYPE_DC,
    'store': STOCK_TYPE_STORE,
    'other': STOCK_TYPE_OTHER
}

STOCK_TYPE_ON_SELLER = 'on_seller'
STOCK_TYPE_ON_SUPPLIER = 'on_supplier'

NATIONAL_DISTRIBUTION_CENTERS = [300, 350, 400, 991]

AVAILABILITY_NATIONWIDE = 'nationwide'
AVAILABILITY_REGIONAL = 'regional'


class ProductSpecification(Enum):
    size = (1, 'Tamanho')
    volume = (2, 'Volume')
    weight = (3, 'Peso')
    flavor = (4, 'Sabor')
    capacity = (5, 'Capacidade')
    quantity = (6, 'Quantidade')
    inch = (7, 'Polegadas')
    console = (8, 'Console')
    capsule = (9, 'Cápsulas')
    piece = (10, 'Peças')
    operator = (11, 'Operador')
    additional = (12, 'Adicional')
    color = (13, 'Cor')
    side = (14, 'Lados')
    litigation = (15, 'Litragem')
    aroma = (16, 'Aroma')
    potency = (17, 'Potência')
    skin_color = (18, 'Cor de Pele')
    theme = (19, 'Tema')
    voltage = (99, 'Voltagem')

    def __init__(self, id, label):
        self.id = id
        self.label = label

    @classmethod
    def get_by_id(cls, id):
        for ps in ProductSpecification:
            if ps.id == id:
                return ps


SPECIFICATIONS_TYPE_BY_LABEL = {
    'Tamanho': 'size',
    'Volume': 'volume',
    'Peso': 'weight',
    'Sabor': 'flavor',
    'Capacidade': 'capacity',
    'Quantidade': 'quantity',
    'Polegadas': 'inch',
    'Console': 'console',
    'Cápsulas': 'capsule',
    'Peças': 'piece',
    'Operador': 'operator',
    'Adicional': 'additional',
    'Cor': 'color',
    'Lados': 'side',
    'Litragem': 'litigation',
    'Aroma': 'aroma',
    'Cor de Pele': 'skin_color',
    'Tema': 'theme',
    'Voltagem': 'voltage'
}


class EnrichmentEventType(Enum):
    ALL = 'all'
    CLASSIFY = 'classify'
    MATCHING = 'matching'


class MessageStatus(Enum):
    DELAYED = 'delayed'
    ERROR = 'error'
    SUCCESS = 'success'


CONJUNCTIONS = [
    'bem como', 'não obstante', 'como', 'se', 'desde que',
    'quando', 'além disso', 'como também', 'e', 'mas também',
    'nem', 'tanto quanto', 'entretanto', 'mas', 'no entanto',
    'porém', 'senão', 'todavia', 'já', 'ora', 'ou',
    'quer', 'seja', 'assim', 'então', 'logo',
    'pois', 'por conseguinte', 'por isso', 'por isto',
    'portanto', 'porquanto', 'porque', 'que',
    'enquanto', 'já que', 'na medida em que', 'pois', 'pois que',
    'por isso que', 'uma vez que', 'visto como', 'visto que', 'assim como',
    'como se', 'maior que', 'mais que', 'melhor que', 'menor que',
    'menos que', 'pior que', 'que nem', 'tal qual', 'tanto quanto',
    'a despeito de', 'ainda que', 'apesar de que', 'bem que', 'conquanto',
    'em que', 'embora', 'mesmo que', 'muito embora', 'nem que', 'posto que',
    'se bem que', 'a menos que', 'a não ser que', 'caso', 'contanto que',
    'dado que', 'salvo se', 'sem que', 'conforme', 'consoante', 'segundo',
    'de forma que', 'de maneira que', 'de modo que', 'de sorte que', 'tal que',
    'tanto que', 'a fim de que', 'para que', 'à medida que', 'à proporção que',
    'ao passo que', 'quanto mais', 'quanto menos', 'antes que', 'apenas',
    'assim que', 'até que', 'cada vez que', 'depois que', 'logo que', 'mal',
    'sempre que', 'todas as vezes que',
]

PREPOSITIONS = [
    'a', 'de', 'em', 'por', 'per'
]

ARTICLES = [
    'o', 'os', 'a', 'as', 'um', 'uns', 'uma', 'umas',
    'ao', 'aos', 'à', 'às', 'do', 'dos', 'da', 'das',
    'dum', 'duns', 'duma', 'dumas', 'no', 'nos', 'na', 'nas',
    'num', 'nuns', 'numa', 'numas', 'pelo', 'pelos', 'pela', 'pelas'
]

NOT_SORTING_FACTSHEET = 999

_110VOLTS_DESCRIPTION = '110V'
_220VOLTS_DESCRIPTION = '220V'

VOLTAGE_VALUES = {
    '110 volts': _110VOLTS_DESCRIPTION,
    '110volts': _110VOLTS_DESCRIPTION,
    '110 v': _110VOLTS_DESCRIPTION,
    '110v': _110VOLTS_DESCRIPTION,
    '127 volts': _110VOLTS_DESCRIPTION,
    '127volts': _110VOLTS_DESCRIPTION,
    '127 v': _110VOLTS_DESCRIPTION,
    '127v': _110VOLTS_DESCRIPTION,
    '220 volts': _220VOLTS_DESCRIPTION,
    '220volts': _220VOLTS_DESCRIPTION,
    '220 v': _220VOLTS_DESCRIPTION,
    '220v': _220VOLTS_DESCRIPTION,
}


RETRY_EXCEPTIONS = (
    'ProvisionedThroughputExceededException',
    'ThrottlingException'
)

SOURCE_RECLASSIFICATION_PRICE_RULE = 'reclassification_price_rule'
SOURCE_HECTOR = 'hector'
SOURCE_METABOOKS = 'metabooks'
SOURCE_OMNILOGIC = 'magalu'
SOURCE_WAKKO = 'wakko'
SOURCE_TAZ = 'taz'
SOURCE_BACKOFFICE_DATASHEET = 'backoffice_datasheet'
SOURCE_API_LUIZA_PICKUPSTORE = 'api_luiza_pickupstore'
SOURCE_API_LUIZA_EXPRESS_DELIVERY = 'api_luiza_express_delivery'
SOURCE_SMARTCONTENT = 'smartcontent'
SOURCE_DATASHEET = 'datasheet'
SOURCE_GENERIC_CONTENT = 'generic_content'
SOURCE_METADATA_VERIFY = 'metadata_verify'
OMNILOGIC = 'omnilogic'


SCORE_TITLE_CRITERIA = 'title'
SCORE_DESCRIPTION_CRITERIA = 'description'
SCORE_IMAGES_CRITERIA = 'images'
SCORE_REVIEW_COUNT_CRITERIA = 'review_count'
SCORE_REVIEW_RATING_CRITERIA = 'review_rating'
SCORE_OFFER_TITLE_CRITERIA = 'offer_title'
SCORE_FACTSHEET_CRITERIA = 'factsheet'
SCORE_V2 = 'v0_2_0'
SCORE_V3 = 'v0_3_0'
RANGE_TYPE = 'range'

SCORE_DEFAULT_ENTITY = 'default'

BRANCH_DETAIL_CACHE_KEY = 'branch_detail_id_{branch_id}'

AVAILABILITY_IN_STOCK = 'in stock'
AVAILABILITY_OUT_OF_STOCK = 'out of stock'

UNPUBLISHED_MESSAGE = 'Successfully unpublished'
UNPUBLISHED_CODE = 'UNPUBLISHED_SUCCESS'

PRODUCT_WRITER_SUCCESS_MESSAGE = 'Successfully processed on product_writer'
PRODUCT_WRITER_SUCCESS_CODE = 'PRODUCT_WRITER_SUCCESS'

PRODUCT_WRITER_OUT_OF_STOCK_CODE = 'PRODUCT_WRITER_OUT_OF_STOCK_CODE'
PRODUCT_WRITER_OUT_OF_STOCK_MESSAGE = (
    'Product id:{navigation_id} seller_id:{seller_id} sku:{sku} deleted '
    'because it is out of stock for more than {days} days'
)

SUCCESS_FACTSHEET_MESSAGE = 'Successfully sent factsheet'
SUCCESS_FACTSHEET_CODE = 'FACTSHEET_SUCCESS'
FAILURE_FACTSHEET_MESSAGE = 'Failed sending factsheet'
FAILURE_FACTSHEET_CODE = 'FACTSHEET_FAILURE'
FACTSHEET_UNFINISHED_PROCESS = 'FACTSHEET_UNFINISHED_PROCESS'
FACTSHEET_SKIP_MESSAGE = 'Skip the update because the factsheet has not changed' # noqa

PRODUCT_EXPORT_SUCCESS_MESSAGE = (
    'Successfully processed on product_exporter with scope {scope}'
)
PRODUCT_EXPORT_SUCCESS_CODE = 'PRODUCT_EXPORTER_{scope}_SUCCESS'

PRODUCT_EXPORT_ERROR_MESSAGE = (
    'Error processing on product export consumer with '
    'scope {scope} error: {error}'
)
PRODUCT_EXPORT_ERROR_CODE = 'PRODUCT_EXPORTER_{scope}_ERROR'

MEDIA_SUCCESS_CODE = 'MEDIA_SUCCESS_CODE'
MEDIA_SUCCESS_MESSAGE = 'Successfully processed medias'
MEDIA_FAILURE_CODE = 'MEDIA_FAILURE_CODE'
MEDIA_FAILURE_MESSAGE = 'Unsuccessfully processed medias'
MEDIA_PARTIAL_ERROR_CODE = 'MEDIA_PARTIAL_ERROR_CODE'
MEDIA_PARTIAL_ERROR_MESSAGE = 'Partially processed medias'
MEDIA_UNFINISHED_PROCESS = 'MEDIA_UNFINISHED_PROCESS'
MEDIA_UNFINISHED_MESSAGE = 'Media unmodified or not available'

PRODUCT_ALREADY_DISABLED_CODE = 'PRODUCT_ALREADY_DISABLED'
PRODUCT_ALREADY_DISABLED_MESSAGE = 'Skip successfully processed on product consumer because product was already disable' # noqa
PRODUCT_SUCCESS_MESSAGE = 'Successfully processed on product consumer'
PRODUCT_SUCCESS_CODE = 'PRODUCT_SUCCESS'
PRODUCT_ERROR_MESSAGE = 'Error processing on product consumer'
PRODUCT_ERROR_CODE = 'PRODUCT_ERROR'
PRODUCT_WRITER_ERROR_CODE = 'PRODUCT_WRITER_ERROR'
PRODUCT_WRITER_UNFINISHED_PROCESS_CODE = 'PRODUCT_WRITER_UNFINISHED_PROCESS'
PRODUCT_WRITER_PRICE_NOT_FOUND_CODE = 'PRODUCT_WRITER_PRICE_NOT_FOUND'
PRODUCT_WRITER_PRICE_NOT_FOUND_MESSAGE = 'Product will not be published because it has no price yet.' # noqa
PRODUCT_WRITER_NO_CORRELATION_FOUND_CODE = 'PRODUCT_WRITER_NO_CORRELATION_FOUND' # noqa
PRODUCT_WRITER_NO_CORRELATION_FOUND_MESSAGE = 'Product will be unpublished because it no longer correlates with previous products.' # noqa
PRODUCT_WRITER_NO_UNIFIED_OBJECT_CODE = 'PRODUCT_WRITER_NO_UNIFIED_OBJECT'
PRODUCT_WRITER_NO_UNIFIED_OBJECT_MESSAGE = 'Product will not be published because it was not assemble with any matching strategy yet.' # noqa
PRODUCT_WRITER_PRODUCT_DISABLE_CODE = 'PRODUCT_WRITER_PRODUCT_DISABLE'
PRODUCT_WRITER_PRODUCT_DISABLE_MESSAGE = 'Product will be unpublished because it has been disabled' # noqa
PRODUCT_UNFINISHED_PROCESS_CODE = 'PRODUCT_UNFINISHED_PROCESS'
PRODUCT_UNFINISHED_PROCESS_MESSAGE = (
    'Couldn\'t finish processing sku:{sku} seller_id:{seller_id} '
    'reason: {reason}'
)
PRODUCT_SKIP_PROCESS = 'Skip the update because the payload has not changed'

PRICE_SUCCESS_MESSAGE = 'Successfully processed on price consumer'
PRICE_SUCCESS_CODE = 'PRICE_SUCCESS'
PRICE_ERROR_MESSAGE = 'Error processing on price consumer'
PRICE_ERROR_CODE = 'PRICE_ERROR'
PRICE_UNFINISHED_PROCESS = 'PRICE_UNFINISHED_PROCESS'

STOCK_SUCCESS_MESSAGE = 'Successfully processed on stock consumer'
STOCK_SUCCESS_CODE = 'STOCK_SUCCESS'
STOCK_ERROR_MESSAGE = 'Error processing on stock consumer'
STOCK_ERROR_CODE = 'STOCK_ERROR'
STOCK_UNFINISHED_PROCESS = 'STOCK_UNFINISHED_PROCESS'

MAAS_PRODUCT_INACTIVATION_SELLER_SUCCESS_CODE = 'MAAS_PRODUCT_INACTIVATION_SELLER_SUCCESS'  # noqa

REDIS_KEY_FORBIDDEN_TERMS = 'forbidden_terms'

NIAGARA = 'niagara'

TETRIX = 'tetrix'

USER_REVIEW_CACHE_KEY_PREFIX = 'user_review_{seller_id}_{sku}'


class GenericContentName(Enum):
    code_anatel = 'Certificado homologado pela Anatel número'


NON_DOWNLOADABLE_MEDIA_TYPES = ('videos',)
NON_UPLOADABLE_MEDIA_TYPES = ('videos',)
VALID_MEDIA_TYPES = ('images', 'audios', 'podcasts', 'videos')

GOOGLE_CLOUD_NAME = 'gcp'
AZION_CLOUD_NAME = 'edge'
