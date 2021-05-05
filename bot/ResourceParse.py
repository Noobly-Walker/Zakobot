import discord
from discord.ext import commands
import sys
import math

from bot.UserData import *
from bot.NumberCronch import *
from data import FileHandler

emojidata = {
    '0020' : '<:0020:771702581038284850>',
    '0021' : '<:0021:771702580501807174>',
    '0022' : '<:0022:771702580501807124>',
    '0023' : '<:0023:771702580438761474>',
    '0024' : '<:0024:771702580350943233>',
    '0025' : '<:0025:771702580770242570>',
    '0026' : '<:0026:771702580799471646>',
    '0027' : '<:0027:771702580777582642>',
    '0028' : '<:0028:771702581160443924>',
    '0029' : '<:0029:771702581000405032>',
    '002A' : '<:002A:771702578392203294>',
    '002B' : '<:002B:771702578425495582>',
    '002C' : '<:002C:771702578554601482>',
    '002D' : '<:002D:771702578673090560>',
    '002E' : '<:002E:771702579386253323>',
    '002F' : '<:002F:771702580279509013>',
    '0030' : '<:0030:771702580929101834>',
    '0031' : '<:0031:771721220525391882>',
    '0032' : '<:0032:771702581110112286>',
    '0033' : '<:0033:771702581134622770>',
    '0034' : '<:0034:771706485599895563>',
    '0035' : '<:0035:771706486048948224>',
    '0036' : '<:0036:771706486127984681>',
    '0037' : '<:0037:771706486161276958>',
    '0038' : '<:0038:771706486337437736>',
    '0039' : '<:0039:771706486481092659>',
    '003A' : '<:003A:771706372663935026>',
    '003B' : '<:003B:771706372847829002>',
    '003C' : '<:003C:771706374236405760>',
    '003D' : '<:003D:771706374203637782>',
    '003E' : '<:003E:771706374244532233>',
    '003F' : '<:003F:771706374375473162>',
    '0040' : '<:0040:771706486611116042>',
    '0041' : '<:0041:771706486861987840>',
    '0042' : '<:0042:771706486861725697>',
    '0043' : '<:0043:771706488137449484>',
    '0044' : '<:0044:771706489215516682>',
    '0045' : '<:0045:771706488921784331>',
    '0046' : '<:0046:771706488858607629>',
    '0047' : '<:0047:771706489222987786>',
    '0048' : '<:0048:771706488997019648>',
    '0049' : '<:0049:771706489085624320>',
    '004A' : '<:004A:771706374437994496>',
    '004B' : '<:004B:771706374585188382>',
    '004C' : '<:004C:771706375440826368>',
    '004D' : '<:004D:771706375330857050>',
    '004E' : '<:004E:771706375033323533>',
    '004F' : '<:004F:771706375465730048>',
    '0050' : '<:0050:771706489189433374>',
    '0051' : '<:0051:771706489136087041>',
    '0052' : '<:0052:771706489260736512>',
    '0053' : '<:0053:771706488623202315>',
    '0054' : '<:0054:771706489227182100>',
    '0055' : '<:0055:771706489198870548>',
    '0056' : '<:0056:771706489282232330>',
    '0057' : '<:0057:771706489176981514>',
    '0058' : '<:0058:771706489244352543>',
    '0059' : '<:0059:771706489249333298>',
    '005A' : '<:005A:771706375424180224>',
    '005B' : '<:005B:771706730370564146>',
    '005C' : '<:005C:771706730429284382>',
    '005D' : '<:005D:771706730580934666>',
    '005E' : '<:005E:771706730404773929>',
    '005F' : '<:005F:771706730915692615>',
    '0060' : '<:0060:771706731481923614>',
    '0061' : '<:0061:771722040683659294>',
    '0062' : '<:0062:771722040947376178>',
    '0063' : '<:0063:771722040579325983>',
    '0064' : '<:0064:771722040658100244>',
    '0065' : '<:0065:771722040826789948>',
    '0066' : '<:0066:771722040902287390>',
    '0067' : '<:0067:771722041161154580>',
    '0068' : '<:0068:771722041262342184>',
    '0069' : '<:0069:771722042306723861>',
    '006A' : '<:006A:771721909502083103>',
    '006B' : '<:006B:771721954838708284>',
    '006C' : '<:006C:771721954846572545>',
    '006D' : '<:006D:771721954771730483>',
    '006E' : '<:006E:771721955115925514>',
    '006F' : '<:006F:771721954523611207>',
    '0070' : '<:0070:771722042545537035>',
    '0071' : '<:0071:771722042898513920>',
    '0072' : '<:0072:771722042583810068>',
    '0073' : '<:0073:771722042520502312>',
    '0074' : '<:0074:771722042260455435>',
    '0075' : '<:0075:771722042369638401>',
    '0076' : '<:0076:771722042360856608>',
    '0077' : '<:0077:771722042344472627>',
    '0078' : '<:0078:771722042604519474>',
    '0079' : '<:0079:771722042336477195>',
    '007A' : '<:007A:771721954972794880>',
    '007B' : '<:007B:771706730958422016>',
    '007C' : '<:007C:771706731185045534>',
    '007D' : '<:007D:771706731042177065>',
    '007E' : '<:007E:771706731151491093>',
    'oc2_1r' : '<:1r:673553297583505408>',
    'oc2_2r' : '<:2r:673553298393006093>',
    'oc2_5r' : '<:5r:673553386876043276>',
    'oc2_10r' : '<:10r:673553387572297728>',
    'oc2_20r' : '<:20r:673553387974819852>',
    'oc2_50r' : '<:50r:673553389258407998>',
    'oc2_100r' : '<:100r:673553389367459870>',
    'oc2_200r' : '<:200r:673553389199818757>',
    'oc2_500r' : '<:500r:673556513612103690>',
    'oc2_1kr' : '<:1kr:673553297680105502>',
    'oc2_2kr' : '<:2kr:673553298091147295>',
    'oc2_5kr' : '<:5kr:673553387035295759>',
    'oc2_10kr' : '<:10kr:673553387282759681>',
    'oc2_20kr' : '<:20kr:673553387823824897>',
    'oc2_50kr' : '<:50kr:673553387853447199>',
    'oc2_100kr' : '<:100kr:673553389233111071>',
    'oc2_200kr' : '<:200kr:673553389539295291>',
    'oc2_500kr' : '<:500kr:673556473346785281>',
    'oc2_1Mr' : '<:1Mr:673553297784832035>',
    'oc2_2Mr' : '<:2Mr:673553298246205450>',
    'oc2_5Mr' : '<:5Mr:673553387106729985>',
    'oc2_10Mr' : '<:10Mr:673553387262050346>',
    'oc2_20Mr' : '<:20Mr:673553388079677481>',
    'oc2_50Mr' : '<:50Mr:673553388532793364>',
    'oc2_100Mr' : '<:100Mr:673553389388300292>',
    'oc2_200Mr' : '<:200Mr:673553389375848469>',
    'oc2_500Mr' : '<:500Mr:673556495467675658>',
    'oc2_1Br' : '<:1Br:673553297629773854>',
    'oc2_2Br' : '<:2Br:673553298011193406>',
    'oc2_5Br' : '<:5Br:673553389082378315>',
    'oc2_10Br' : '<:10Br:673553387467440195>',
    'oc2_20Br' : '<:20Br:673553387735875594>',
    'oc2_50Br' : '<:50Br:673553388012568582>',
    'oc2_100Br' : '<:100Br:673553389325385729>',
    'oc2_200Br' : '<:200Br:673553389547683905>',
    'oc2_500Br' : '<:500Br:673553389585432628>',
    'oc2_1Tr' : '<a:1Tr:650866517638119454>',
    'oc2_kup' : '<:kup:673559517010722865>',
    'oc2_arg' : '<:arg:673559516645949460>',
    'oc2_auru' : '<:auru:673559516494692374>',
    'oc2_pletus' : '<:pletus:673559516993814568>',
    'oc2_pluot' : '<:pluot:817236751110111232>',
    'oc2_kaali' : '<:kaali:673559516964585490>',
    'oc2_clover' : '<:clover:673559516599812177>',
    'oc2_field' : '<:field:673559517320970290>',
    'oc2_ay' : '<:ay:673560644766662656>',
    'oc2_be' : '<:be:673560644426924075>',
    'oc2_che' : '<:che:673559516427845644>',
    'oc2_ce' : '<:ce:673560644812931083>',
    'oc2_de' : '<:de:673560644661936158>',
    'oc2_eh' : '<:eh:673560644729045032>',
    'oc2_ef' : '<:ef:673560644754210831>',
    'oc2_ge' : '<:ge:673560644401758221>',
    'oc2_he' : '<:he:673560644834033697>',
    'oc2_thorn' : '<:thorn:673559516952133642>',
    'oc2_ie' : '<:ie:673560644343169031>',
    'oc2_je' : '<:je:673560644485644297>',
    'oc2_ke' : '<:ke:673560644599152651>',
    'oc2_el' : '<:el:673560644532043807>',
    'oc2_em' : '<:em:673560644812800021>',
    'oc2_en' : '<:en:673560644762599428>',
    'oc2_oh' : '<:oh:673560644821188668>',
    'oc2_pe' : '<:pe:673560644754079765>',
    'oc2_qe' : '<:qe:673560645257527326>',
    'oc2_ar' : '<:ar:673560644464934944>',
    'oc2_es' : '<:es:673560644817256448>',
    'oc2_te' : '<:te:673560645152538654>',
    'oc2_uh' : '<:uh:673560644834033674>',
    'oc2_ve' : '<:ve:673560644829839397>',
    'oc2_wa' : '<:wa:673560644993155083>',
    'oc2_ex' : '<:ex:673560645110726671>',
    'oc2_wy' : '<:wy:673560645136023565>',
    'oc2_ze' : '<:ze:673560644917919745>',
    'oc2_voed' : '<:voed:673560644460740620>',
    'oc2_pont' : '<:pont:673560835569877007>',
    'oc2_koma' : '<:koma:673560835448111104>',
    'oc2_un' : '<:un:673560645077303318>',
    'oc2_duo' : '<:duo:673560644573986826>',
    'oc2_tre' : '<:tre:673560644573724752>',
    'oc2_qad' : '<:qad:673560644527718401>',
    'oc2_pent' : '<:pent:673560644322328578>',
    'oc2_hex' : '<:hex:673560644666130443>',
    'oc2_sept' : '<:sept:673560644653547550>',
    'oc2_okt' : '<:okt:673560644381048863>',
    'oc2_enn' : '<:enn:673560644775313440>',
    'oc2_nil' : '<:nil:673560644447895593>',
    'oc2_lcd?' : '<:lcdQUEST:756998225998905444>',
    'oc2_lcd!' : '<:lcdEXCLAM:756998225671618581>',
    'oc2_lcd;' : '<:lcdSEMICOL:756998225671749723>',
    'oc2_lcd:' : '<:lcdCOLON:756998225612898378>',
    'oc2_lcd/' : '<:lcdSLASH:756998225818288139>',
    'oc2_lcd\\' : '<:lcdBSLASH:756998225554309284>',
    'oc2_lcd-' : '<:lcdHYPH:756998225877270600>',
    'oc2_lcd_' : '<:lcdUNDERSCOR:756998226048974990>',
    'oc2_lcd(' : '<:lcdOPENPAR:756998225642389646>',
    'oc2_lcd)' : '<:lcdCLOSPAR:756998225868881991>',
    'oc2_lcd{' : '<:lcdOPENCURL:756998225621287074>',
    'oc2_lcd}' : '<:lcdCLOSECURL:756998225927602288>',
    'oc2_lcd+' : '<:lcdPLUS:756998225982128240>',
    'oc2_lcd#' : '<:lcdHASH:757006921961177139>',
    'oc2_lcd%' : '<:lcdPERCENT:757006921898393652>',
    'oc2_lcd^' : '<:lcdKARAT:757006922196189316>',
    'oc2_lcd&' : '<:lcdAMP:757010300154150973>',
    'oc2_lcd*' : '<:lcdASTER:757006922288201808>',
    'oc2_lcd[' : '<:lcdOPENBR:757006921927622730>',
    'oc2_lcd]' : '<:lcdCLOSEBR:757013527952228402>',
    'oc2_lcd|' : '<:lcdBAR:757006922321887313>',
    'oc2_lcd=' : '<:lcdEQUAL:757006922233938050>',
    'oc2_lcd\'' : '<:lcdAPOST:757006922032611401>',
    'oc2_lcd"' : '<:lcdQUOTE:757006922439458898>',
    'oc2_lcdDOLLAR' : '<:lcdDOLLAR:757006923944951868>',
    'oc2_lcdPOUND' : '<:lcdPOUND:757006922313629728>',
    'oc2_lcdYEN' : '<:lcdYEN:757006922103652404>',
    'oc2_lcdINF' : '<:lcdINF:673560835427270666>',
    'oc2_accuse' : '<:accuse:615693369217384468>',
    'oc2_badtime' : '<:badtime:606425716556300308>',
    'oc2_FatThunk' : '<:FatThunk:606425982290624525>',
    'oc2_omnicore' : '<:omnicore:688929986018672702>',
    'oc2_oof' : '<:oof:652768776013611038>',
    'oc2_OOF' : '<:OOF:652768634472497172>',
    'oc2_PhatThunk' : '<:PhatThunk:606426015840993291>',
    'oc2_shit' : '<:shit:629728743673430035>',
    'oc2_six_shooter' : '<:six_shooter:644544991955386400>',
    'oc2_imgmeow' : '<:imgmeow:669735379028410378>',
    'oc2_triggered' : '<:triggered:275430296101584897>',
    'oc2_temnoob' : '<:temnoob:273684372622934018>',
    'oc2_squidkid' : '<:squidkid:275430216254488577>',
    'oc2_Poopachu' : '<:Poopachu:279809361268965376>',
    'oc2_Pikatonball' : '<:Pikatonball:258240344515149824>',
    'oc2_Noobly' : '<:Noobly:258243900827893771>',
    'oc2_MysteryChibbs' : '<:MysteryChibbs:276869367873011722>',
    'oc2_LV' : '<:LV:271762118242467851>',
    'oc2_lenny' : '<:lenny:276869084073951244>',
    'oc2_JizzFace' : '<:JizzFace:281995889810210826>',
    'oc2_IMGOINGTOKILLYOU' : '<:IMGOINGTOKILLYOU:276856902502187008>',
    'oc2_DT' : '<:DT:271761470004396033>',
    'oc2_badtom' : '<:badtom:267751451378319390>',
    'oc2_5th_age_legendary' : '<:5th_age_legendary:669908525392199690>',
    'oc2_6th_age_legendary' : '<:6th_age_legendary:669908524259868693>',
    'oc2_7th_age_legendary' : '<:7th_age_legendary:669908524469583872>',
    'oc2_nitroboost' : '<:nitroboost:672192010488381450>',
    'oc2_occ' : '<:occ:688929850194788378>',
    'oc2_meow' : '<a:meow:669735352277139486>',
    'oc2_eviely_hoi_a' : '<a:Eviely_hoi_a:650861281682653225>',
    'oc2_half_star' : '<:half_star:688929776484089967>',
    'oc2_black_star' : '<:black_star:682326690499919929>',
    'oc2_ugh' : '<:ugh:694992145689477251>',
    "oc2_msw1": "<:msw1:739810675747979314>",
    "oc2_msw2": "<:msw2:739810675827933274>",
    "oc2_msw3": "<:msw3:739810675844448367>",
    "oc2_msw4": "<:msw4:739810675584663576>",
    "oc2_msw5": "<:msw5:739810675819413625>",
    "oc2_msw6": "<:msw6:739810675878264872>",
    "oc2_msw7": "<:msw7:739810675685064815>",
    "oc2_msw8": "<:msw8:739810675819413614>",
    "oc2_tetrate": "<:tetrate:702477107007062087>",
    "oc2_dab": "<:dab:776879980307152926>",
    'f3rpm_wassat' : '<:wassat:453677268586201099>',
    'f3rpm_suuuuure' : '<:suuuuure:445721007341174794>',
    'f3rpm_Soon' : '<:Soon:441788958980964365>',
    'f3rpm_playtime' : '<:playtime:441801199520579584>',
    'f3rpm_OOH' : '<:OOH:453676766167433251>',
    'f3rpm_mercyme' : '<:mercyme:451257452609142805>',
    'f3rpm_megacackle' : '<:megacackle:445387159906680842>',
    'f3rpm_makesyathink' : '<:makesyathink:445370888330674176>',
    'f3rpm_maid' : '<:maid:451257423290957855>',
    'f3rpm_Lurk' : '<:Lurk:441791777175764992>',
    'f3rpm_lecture' : '<:lecture:441791730824642561>',
    'f3rpm_lawl' : '<:lawl:441789843534643201>',
    'f3rpm_kappa' : '<:kappa:447225926657507338>',
    'f3rpm_humpday' : '<:humpday:442598395526512641>',
    'f3rpm_howexciting' : '<:howexciting:441790025567567872>',
    'f3rpm_HMM' : '<:HMM:447225901931954177>',
    'f3rpm_feish' : '<:feish:445373125224431618>',
    'f3rpm_facehoof' : '<:facehoof:441791896872812545>',
    'f3rpm_eep' : '<:eep:441789766636142592>',
    'f3rpm_dorgon' : '<:dorgon:441789879941070858>',
    'f3rpm_blech' : '<:blech:441789818079543296>',
    'atb4_silvereevee' : '<:silvereevee:543420779556241408>',
    'atb4_missingtextureeevee' : '<:missingtextureeevee:541895676217524224>',
    'atb4_goldeevee' : '<:goldeevee:541405995922882585>',
    'atb4_eevee' : '<:eevee:541405995612635147>',
    'atb4_coppereevee' : '<:coppereevee:541405995901911060>',
    'atb4_ayee' : '<:ayee:411167470624178177>',
    'atb0_you_dont_say' : '<:AT_you_dont_say:317285059843457026>',
    'atb0_triggered' : '<:AT_triggered:317285310918819840>',
    'atb0_o_rly' : '<:AT_o_rly:317285230992031744>',
    'atb0_lenny' : '<:AT_lenny:317284955346698240>',
    'atb0_kappa_storm' : '<:AT_kappa_storm:317284888585961473>',
    'atb0_jhon_cena' : '<:AT_jhon_cena:317284924040282113>',
    'atb0_impossibru' : '<:AT_impossibru:317285456280813568>',
    'atb0_golden_pepe' : '<:AT_golden_pepe:317284839890092035>'}
rupeeType = {
    1 : emojidata['oc2_1r'],
    2 : emojidata['oc2_2r'],
    5 : emojidata['oc2_5r'],
    10 : emojidata['oc2_10r'],
    20 : emojidata['oc2_20r'],
    50 : emojidata['oc2_50r'],
    100 : emojidata['oc2_100r'],
    200 : emojidata['oc2_200r'],
    500 : emojidata['oc2_500r'],
    1000 : emojidata['oc2_1kr'],
    2000 : emojidata['oc2_2kr'],
    5000 : emojidata['oc2_5kr'],
    10000 : emojidata['oc2_10kr'],
    20000 : emojidata['oc2_20kr'],
    50000 : emojidata['oc2_50kr'],
    100000 : emojidata['oc2_100kr'],
    200000 : emojidata['oc2_200kr'],
    500000 : emojidata['oc2_500kr'],
    1000000 : emojidata['oc2_1Mr'],
    2000000 : emojidata['oc2_2Mr'],
    5000000 : emojidata['oc2_5Mr'],
    10000000 : emojidata['oc2_10Mr'],
    20000000 : emojidata['oc2_20Mr'],
    50000000 : emojidata['oc2_50Mr'],
    100000000 : emojidata['oc2_100Mr'],
    200000000 : emojidata['oc2_200Mr'],
    500000000 : emojidata['oc2_500Mr'],
    1000000000 : emojidata['oc2_1Br'],
    2000000000 : emojidata['oc2_2Br'],
    5000000000 : emojidata['oc2_5Br'],
    10000000000 : emojidata['oc2_10Br'],
    20000000000 : emojidata['oc2_20Br'],
    50000000000 : emojidata['oc2_50Br'],
    100000000000 : emojidata['oc2_100Br'],
    200000000000 : emojidata['oc2_200Br'],
    500000000000 : emojidata['oc2_500Br'],
    1000000000000 : emojidata['oc2_1Tr']
    }
coinType = {
    0.001 : emojidata['oc2_kup'],
    1 : emojidata['oc2_arg'],
    1000 : emojidata['oc2_auru'],
    1000000 : emojidata['oc2_pluot'],
    1000000000 : emojidata['oc2_kaali']
    }

def rupEmojFind(rupees): # A function that takes a variable representing an amount of rupees, and finds an emoji representative of the amount
    rupees = abs(rupees)
    rupeeEmote = rupeeType[1]
    for key in rupeeType.keys():
        if rupees >= key:
            rupeeEmote = rupeeType[key]
    return rupeeEmote

def coinEmojFind(coins): # A function that takes a variable representing an amount of rupees, and finds an emoji representative of the amount
    coins = abs(coins)
    coinEmote = coinType[0.001]
    for key in coinType.keys():
        if coins >= key:
            coinEmote = coinType[key]
    return coinEmote

def compress(rupees: int, coins: int, clovers: int, land: int, *userid):
    rupeeMessage, coinMessage, cloverMessage, deedMessage = '', '', '', ''
    # --- Building Output Strings --- #
    rupeeMessage = compress_rup_clov(rupees, 'rupee', *userid) + ', '
    coinMessage = compress_coin(coins, *userid) + ', '
    cloverMessage = compress_rup_clov(clovers, 'oc2_clover', *userid) + ', '
    deedMessage = compress_land(land)
    returnMsg = rupeeMessage + coinMessage + cloverMessage + deedMessage
    return returnMsg

def compress_rup_clov(var: int, icon, *userid):
    if len(userid) == 0:
        var_cronch = number_cronch(var, 405968021337669632)
    else:
        var_cronch = number_cronch(var, userid[0])
    if icon == 'rupee':
        iconout = rupEmojFind(var)
    else:
        iconout = emojidata[icon]
    var = round(var)
    out = iconout + var_cronch
    return out

def compress_land(land: int):
    icon = emojidata['oc2_field']
    land = round(land)
    out = ''
    if is_infinite(land) == True:
        out = icon + 'Float ∞'
    elif is_infinite(land) == False:
        if land > 100:
            land /= 100
            if land < 100:
                out = icon + '{0} hectares'.format(round(land, 3))
            elif land > 100:
                land /= 100
                if land < 1000000:
                    out = icon + '{0} km²'.format(round(land, 3))
                elif land > 1000000:
                    land /= 1000000
                    out = icon + '{0} Mm²'.format(round(land, 3))
        elif land > 1:
            out = icon + '{0} acres'.format(round(land, 3))
        elif land == 1:
            out = icon + '1 acre'
        elif land == 0:
            out = icon + '0 acres'
    return out

def compress_coin(coins: int, *userid):
    if len(userid) == 0:
        notation = 0
    else:
        data = FileHandler.get_user_data(userid[0])
        notation = data.notation()
    if is_infinite(coins) == True or coins >= 1000000000:
        coinHandle = infinityOverflow(coins)
        coins = coinHandle[0]
        coink = coinHandle[1]-3
        out = coinType[1000000000] + notatize(coins, coink, notation)
    elif is_infinite(coins) == False:
        if abs(coins) < 1000:
            coins = round(coins, 3)
            out = coinType[0.001] + str(coins)
        elif abs(coins) >= 1000:
            coins /= 1000
            coins = round(coins, 3)
            if abs(coins) < 1000:
                out = coinType[1] + str(coins)
            elif abs(coins) >= 1000:
                coins /= 1000
                coins = round(coins, 3)
                if abs(coins) < 1000:
                    out = coinType[1000] + str(coins)
                elif abs(coins) >= 1000:
                    coins /= 1000
                    coins = round(coins, 3)
                    if abs(coins) < 1000:
                        out = coinType[1000000] + str(coins)
                    elif abs(coins) >= 1000:
                        coins /= 1000
                        coins = round(coins, 3)
                        if abs(coins) < 1000:
                            out = coinType[1000000000] + str(coins)
    return out

def multi_compress(pcomp, acomp, mcomp, ccomp, power, *userid):
    pmessage, amessage, mmessage, cmessage, powmessage = '', '', '', '', ''
    # --- Building Output Strings --- #
    pmessage = number_cronch(pcomp, userid) + ' Mining Durability, '
    amessage = number_cronch(acomp, userid) + ' Chopping Durability, '
    mmessage = number_cronch(mcomp, userid) + ' Money Multi, '
    cmessage = str(ccomp) + ' Counting Multi, '
    powmessage = number_cronch(power, userid) + ' Military Power'
    returnMsg = pmessage + amessage + '\n' + mmessage + cmessage + powmessage
    return returnMsg
