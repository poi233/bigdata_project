# -*- coding: UTF-8 -*-
import json
import os
import re

from pyspark import SparkContext

label_list = ['person_name', 'business_name', 'phone_number', 'address', 'street_name', 'city', 'neighborhood',
              'lat_lon_cord', 'zip_code', 'borough', 'school_name', 'color', 'car_make', 'city_agency', 'area_of_study',
              'subject_in_school', 'school_level', 'college_name', 'website', 'building_classification', 'vehicle_type',
              'location_type', 'park_playground', 'other']

cities = """accord,adams village,adams center,addison village,afton village,airmont village,akron village,albany,albertson,albion village,alden village,alexander village,alexandria bay village,alfred village,allegany village,almond village,altamont village,altmar village,altona,amagansett,amenia,ames village,amityville village,amsterdam,andes village,andover village,angelica village,angola village,angola on the lake,antwerp village,apalachin,aquebogue,arcade village,ardsley village,argyle village,arkport village,arlington,armonk,asharoken village,athens village,atlantic beach village,attica village,auburn,aurora village,au sable forks,averill park,avoca village,avon village,babylon village,bainbridge village,baiting hollow,baldwin,baldwin harbor,baldwinsville village,ballston spa village,balmville,bardonia,barker village,barneveld village,barnum island,batavia,bath village,baxter estates village,bay park,bayport,bay shore,bayville village,baywood,beacon,beaverdam lake-salisbury mills,bedford,bellerose village,bellerose terrace,belle terre village,bellmore,bellport village,belmont village,bemus point village,bergen village,bethpage,big flats,big flats airport,billington heights,binghamton,black river village,blasdell village,blauvelt,bloomfield village,bloomingburg village,blue point,bohemia,bolivar village,boonville village,brasher falls-winthrop,brentwood,brewerton,brewster village,brewster hill,briarcliff manor village,bridgehampton,bridgeport,bridgewater village,brighton,brightwaters village,brinckerhoff,broadalbin village,brockport village,brocton village,bronxville village,brookhaven,brookville village,brownville village,brushton village,buchanan village,buffalo,burdett village,burke village,cairo,calcium,caledonia village,callicoon,calverton,cambridge village,camden village,camillus village,canajoharie village,canandaigua,canaseraga village,canastota village,candor village,canisteo village,canton village,cape vincent village,carle place,carmel hamlet,carthage village,cassadaga village,castile village,castleton-on-hudson village,castorland village,cato village,catskill village,cattaraugus village,cayuga village,cayuga heights village,cazenovia village,cedarhurst village,celoron village,centereach,center moriches,centerport,central islip,central square village,central valley,centre island village,champlain village,chappaqua,chateaugay village,chatham village,chaumont village,cheektowaga,cherry creek village,cherry valley village,chester village,chestnut ridge village,chittenango village,churchville village,clarence center,clark mills,claverack-red mills,clayton village,clayville village,cleveland village,clifton springs village,clinton village,clintondale,clyde village,cobleskill village,coeymans,cohocton village,cohoes,cold brook village,cold spring village,cold spring harbor,colonie village,commack,congers,constableville village,constantia,cooperstown village,copake lake,copenhagen village,copiague,coram,corfu village,corinth village,corning,cornwall on hudson village,cortland,cortland west,country knolls,cove neck village,coxsackie village,cragsmoor,croghan village,crompond,croton-on-hudson village,crown heights,crugers,cuba village,cumberland head,cutchogue,dannemora village,dansville village,deer park,deferiet village,delanson village,delevan village,delhi village,delmar,depauville,depew village,deposit village,dering harbor village,deruyter village,dexter village,dix hills,dobbs ferry village,dolgeville village,dover plains,dresden village,dryden village,duane lake,duanesburg,dundee village,dunkirk,earlville village,east atlantic beach,east aurora village,eastchester,east farmingdale,east garden city,east glenville,east greenbush,east hampton village,east hampton north,east hills village,east islip,east ithaca,east kingston,east marion,east massapequa,east meadow,east moriches,east nassau village,east northport,east norwich,east patchogue,eastport,east quogue,east randolph village,east rochester village,east rockaway village,east shoreham,east syracuse village,east williston village,eatons neck,eden,edwards village,elba village,elbridge village,ellenville village,ellicottville village,ellisburg village,elma center,elmira,elmira heights village,elmont,elmsford village,elwood,endicott village,endwell,esperance village,evans mills village,fabius village,fair haven village,fairmount,fairport village,fairview cdp (dutchess county),fairview cdp (westchester county),falconer village,farmingdale village,farmingville,farnham village,fayetteville village,fire island,firthcliffe,fishers island,fishkill village,flanders,fleischmanns village,floral park village,florida village,flower hill village,fonda village,forest home,forestville village,fort ann village,fort drum,fort edward village,fort johnson village,fort montgomery,fort plain village,fort salonga,frankfort village,franklin village,franklin square,franklinville village,fredonia village,freeport village,freeville village,frewsburg,friendship,fulton,fultonville village,gainesville village,galeville,galway village,gang mills,garden city village,garden city park,garden city south,gardiner,gardnertown,gasport,gates-north gates,geneseo village,geneva,germantown,ghent,gilbertsville village,gilgo-oak beach-captree,glasco,glen cove,glen head,glen park village,glens falls,glens falls north,glenwood landing,gloversville,golden's bridge,gordon heights,goshen village,gouverneur village,gowanda village,grand view-on-hudson village,granville village,great bend,great neck village,great neck estates village,great neck gardens,great neck plaza village,great river,greece,greene village,green island village,greenlawn,greenport village,greenport west,greenvale,greenville cdp (greene county),greenville cdp (westchester county),greenwich village,greenwood lake village,groton village,hagaman village,halesite,hamburg village,hamilton village,hammond village,hammondsport village,hampton bays,hampton manor,hancock village,hannibal village,harbor hills,harbor isle,harriman village,harris hill,harrison village,harrisville village,hartsdale,hastings-on-hudson village,hauppauge,haverstraw village,haviland,hawthorne,head of the harbor village,hempstead village,heritage hills,herkimer village,hermon village,herricks,herrings village,heuvelton village,hewlett,hewlett bay park village,hewlett harbor village,hewlett neck village,hicksville,high falls,highland,highland falls village,highland mills,hillburn village,hillcrest,hillside,hillside lake,hilton village,hobart village,holbrook,holland,holland patent village,holley village,holtsville,homer village,honeoye falls village,hoosick falls village,hopewell junction,hornell,horseheads village,horseheads north,houghton,hudson,hudson falls village,hunter village,huntington,huntington bay village,huntington station,hurley,ilion village,interlaken village,inwood,irondequoit,irvington village,islandia village,island park village,islip,islip terrace,ithaca,jamesport,jamestown,jamestown west,jefferson heights,jefferson valley-yorktown,jeffersonville village,jericho,johnson city village,johnstown,jordan village,kaser village,keeseville village,kenmore village,kensington village,kerhonkson,kinderhook village,kings park,kings point village,kingston,kiryas joel village,lackawanna,lacona village,la fargeville,lake carmel,lake erie beach,lake george village,lake grove village,lake katrine,lakeland,lake luzerne-hadley,lake mohegan,lake placid village,lake ronkonkoma,lake success village,lakeview,lakewood village,lancaster village,lansing village,larchmont village,lattingtown village,laurel,laurel hollow village,laurens village,lawrence village,leeds,leicester village,le roy village,levittown,lewiston village,liberty village,lido beach,lima village,lime lake-machias,limestone village,lincolndale,lincoln park,lindenhurst village,lisle village,little falls,little valley village,liverpool village,livingston manor,livonia village,lloyd harbor village,lockport,locust valley,lodi village,long beach,lorenz park,lowville village,lynbrook village,lyncourt,lyndonville village,lyon mountain,lyons village,lyons falls village,macedon village,mcgraw village,madison village,mahopac,malden,malone village,malverne village,malverne park oaks,mamaroneck village,manchester village,manhasset,manhasset hills,manlius village,mannsville village,manorhaven village,manorville,marathon village,marcellus village,margaretville village,mariaville lake,marlboro,massapequa,massapequa park village,massena village,mastic,mastic beach,matinecock village,mattituck,mattydale,maybrook village,mayfield village,mayville village,mechanicstown,mechanicville,medford,medina village,medusa,melrose park,melville,menands village,meridian village,merrick,mexico village,middleburgh village,middle island,middleport village,middletown,middleville village,milford village,millbrook village,miller place,millerton village,mill neck village,millport village,milton cdp (saratoga county),milton cdp (ulster county),mineola village,minetto,mineville-witherbee,minoa village,mohawk village,monroe village,monsey,montauk,montebello village,montgomery village,monticello village,montour falls village,mooers,moravia village,moriches,morris village,morrisonville,morristown village,morrisville village,mount ivy,mount kisco village,mount morris village,mount sinai,mount vernon,munnsville village,munsey park village,munsons corners,muttontown village,myers corner,nanuet,napanoch,napeague,naples village,narrowsburg,nassau village,natural bridge,nedrow,nelliston village,nelsonville village,nesconset,newark village,newark valley village,new berlin village,newburgh,new cassel,new city,newfane,newfield hamlet,new hartford village,new hempstead village,new hyde park village,new paltz village,newport village,new rochelle,new square village,new suffolk,new windsor,new york,new york mills village,niagara falls,nichols village,niskayuna,nissequogue village,niverville,norfolk,north amityville,northampton,north babylon,north ballston spa,north bay shore,north bellmore,north bellport,north boston,north collins village,northeast ithaca,north great river,north haven village,north hills village,north hornell village,north lindenhurst,north lynbrook,north massapequa,north merrick,north new hyde park,north patchogue,northport village,north sea,north syracuse village,north tonawanda,north valley stream,northville village,northville,north wantagh,northwest harbor,northwest ithaca,norwich,norwood village,noyack,nunda village,nyack village,oakdale,oakfield village,ocean beach village,oceanside,odessa village,ogdensburg,olcott,old bethpage,old brookville village,old field village,old westbury village,olean,oneida,oneida castle village,oneonta,orangeburg,orange lake,orchard park village,orient,oriskany village,oriskany falls village,ossining village,oswego,otego village,otisville village,ovid village,owego village,oxford village,oyster bay,oyster bay cove village,painted post village,palatine bridge village,palenville,palmyra village,panama village,parc,parish village,patchogue village,pattersonville-rotterdam junction,pawling village,peach lake,pearl river,peconic,peekskill,pelham village,pelham manor village,penn yan village,perry village,perrysburg village,peru,phelps village,philadelphia village,philmont village,phoenicia,phoenix village,piermont village,pike village,pine bush,pine hill,pine plains,pittsford village,plainedge,plainview,plandome village,plandome heights village,plandome manor village,plattekill,plattsburgh,plattsburgh west,pleasant valley,pleasantville village,poestenkill,point lookout,poland village,pomona village,poquott village,port byron village,port chester village,port dickinson village,port ewen,port henry village,port jefferson village,port jefferson station,port jervis,port leyden village,portville village,port washington,port washington north village,potsdam village,poughkeepsie,preston-potter hollow,prospect village,pulaski village,putnam lake,quioque,quogue village,randolph village,ransomville,rapids,ravena village,red creek village,redford,red hook village,red oaks mill,redwood,remsen village,remsenburg-speonk,rensselaer,rensselaer falls village,rhinebeck village,richburg village,richfield springs village,richmondville village,richville village,ridge,rifton,ripley,riverhead,riverside village,riverside,rochester,rock hill,rockville centre village,rocky point,rome,ronkonkoma,roosevelt,roscoe,rosendale village,roslyn village,roslyn estates village,roslyn harbor village,roslyn heights,rotterdam,round lake village,rouses point village,rushville village,russell gardens village,rye,rye brook village,sackets harbor village,saddle rock village,saddle rock estates,sagaponack,sag harbor village,st. bonaventure,st. james,st. johnsville village,salamanca,salem village,salisbury,saltaire village,sand ridge,sands point village,sandy creek village,saranac lake village,saratoga springs,saugerties village,saugerties south,savona village,sayville,scarsdale village,schaghticoke village,schenectady,schoharie village,schuylerville village,scotchtown,scotia village,scotts corners,scottsville village,sea cliff village,seaford,searingtown,selden,seneca falls village,seneca knolls,setauket-east setauket,sharon springs village,shelter island,shelter island heights,shenorock,sherburne village,sherman village,sherrill,shinnecock hills,shirley,shokan,shoreham village,shortsville village,shrub oak,sidney village,silver creek village,silver springs village,sinclairville village,skaneateles village,sleepy hollow village,sloan village,sloatsburg village,smallwood,smithtown,smyrna village,sodus village,sodus point village,solvay village,sound beach,southampton village,south corning village,south dayton village,south fallsburg,south farmingdale,south floral park village,south glens falls village,south hempstead,south hill,south huntington,south lockport,south nyack village,southold,southport,south valley stream,spackenkill,speculator village,spencer village,spencerport village,springs,spring valley village,springville village,staatsburg,stamford village,stannards,star lake,stewart manor village,stillwater village,stone ridge,stony brook,stony point,stottville,suffern village,sylvan beach village,syosset,syracuse,tannersville village,tappan,tarrytown village,terryville,theresa village,thiells,thomaston village,thornwood,tillson,tivoli village,tonawanda,tonawanda,town line,tribes hill,troy,trumansburg village,tuckahoe,tuckahoe village,tully village,tupper lake village,turin village,tuxedo park village,unadilla village,uniondale,union springs village,unionville village,university gardens,upper brookville village,upper nyack village,utica,vails gate,valatie village,valhalla,valley cottage,valley falls village,valley stream village,van etten village,vernon village,verplanck,victor village,victory village,village green,village of the branch village,viola,voorheesville village,waddington village,wading river,wainscott,walden village,walker valley,wallkill,walton village,walton park,wampsville village,wantagh,wappingers falls village,warrensburg,warsaw village,warwick village,washington heights,washingtonville village,waterford village,waterloo village,watermill,watertown,waterville village,watervliet,watkins glen village,waverly village,wayland village,webster village,weedsport village,wellsburg village,wellsville village,wesley hills village,west babylon,west bay shore,westbury village,west carthage village,west elmira,west end,westfield village,west glens falls,westhampton,westhampton beach village,west hampton dunes village,west haverstraw village,west hempstead,west hills,west hurley,west islip,westmere,west nyack,weston mills,west point,west sand lake,west sayville,west seneca,westvale,west winfield village,wheatley heights,whitehall village,white plains,whitesboro village,whitney point village,williamsville village,williston park village,wilson village,windham,windsor village,wolcott village,woodbury,woodmere,woodridge village,woodsburgh village,woodstock,wurtsboro village,wyandanch,wynantskill,wyoming village,yaphank,yonkers,yorkshire,yorktown heights,yorkville village,youngstown village,zena"""
counties = """albany,allegany,bronx,broome,cattaraugus,cayuga,chautauqua,chemung,chenango,clinton,columbia,cortland,delaware,dutchess,erie,essex,franklin,fulton,genesee,greene,hamilton,herkimer,jefferson,kings,lewis,livingston,madison,monroe,montgomery,nassau,new york city,niagara,oneida,onondaga,ontario,orange,orleans,oswego,otsego,putnam,queens,rensselaer,richmond,rockland,st. lawrence,saratoga,schenectady,schoharie,schuyler,seneca,steuben,suffolk,sullivan,tioga,tompkins,ulster,warren,washington,wayne,westchester,wyoming,yates"""
borough = "bronx,brooklyn,manhattan,queens,staten island,the bronx,bkly"
borough_ab = "K,M,Q,R,X"
school_levels = "elementary,k-8,middle,high school,high school transfer,k-3,yabc"
park_types = "playground,park,field,garden,senior center,gardens,parkway"
colors = "amber,ash,asphalt,auburn,avocado,aquamarine,azure,beige,bisque,black,blue,bone,bordeaux,brass,bronze,brown,burgundy,camel,caramel,canary,celeste,cerulean,champagne,charcoal,chartreuse,chestnut,chocolate,citron,claret,coal,cobalt,coffee,coral,corn,cream,crimson,cyan,denim,desert,ebony,ecru,emerald,feldspar,fuchsia,gold,gray,green,heather,indigo,ivory,jet,khaki,lime,magenta,maroon,mint,navy,olive,orange,pink,plum,purple,red,rust,salmon,sienna,silver,snow,steel,tan,teal,tomato,violet,white,yellow"
business_pattern = "corp,inc,llc,bar,service,cafe,market,mall,restaurant,taste,pizza,fusion,food"
school_name_pattern = "acad,academic,school,p.s.,i.s.,hs,sped,m.s.,ps/is,j.h.s."
neiborhoods = "bath,beach,allerton,battery,park,city,arverne,annadale,bay,ridge,bathgate,beekman,place,astoria,arden,heights,bedford,stuyvesant,baychester,carnegie,hill,astoria,heights,arlington,bensonhurst,bedford,park,chelsea,auburndale,arrochar,bergen,beach,belmont,chinatown,bay,terrace,bay,terrace,boerum,hill,bronxdale,civic,center,bayside,bloomfield,borough,park,bronx,park,south,clinton,bayswater,bulls,head,brighton,beach,bronx,river,east,harlem,beechhurst,butler,manor,broadway,junction,castle,hill,east,village,bellaire,castleton,corners,brooklyn,heights,city,island,financial,district,belle,harbor,charleston,brownsville,claremont,village,flatiron,bellerose,chelsea,bushwick,clason,point,gramercy,blissville,clifton,canarsie,concourse,greenwich,village,breezy,point,concord,carroll,gardens,concourse,village,hamilton,heights,briarwood,dongan,hills,city,line,co-op,city,harlem,(central),broad,channel,egbertville,clinton,hill,country,club,herald,square,brookville,elm,park,cobble,hill,east,tremont,hudson,square,cambria,heights,eltingville,coney,island,eastchester,inwood,clearview,emerson,hill,crown,heights,edenwald,lenox,hill,college,point,fox,hills,cypress,hills,edgewater,park,lincoln,square,douglaston,graniteville,ditmas,park,fieldston,little,italy,dutch,kills,grant,city,downtown,fordham,lower,east,side,east,elmhurst,grasmere,dumbo,high,bridge,manhattan,valley,edgemere,great,kills,dyker,heights,hunts,point,manhattanville,elmhurst,greenridge,east,flatbush,kingsbridge,midtown,south,far,rockaway,grymes,hill,east,new,york,kingsbridge,heights,midtown,floral,park,heartland,village,east,williamsburg,longwood,morningside,heights,flushing,howland,hook,farragut,marble,hill,murray,hill,flushing,(downtown),huguenot,flatbush,melrose,noho,forest,hills,lighthouse,hill,flatlands,morris,heights,roosevelt,island,forest,hills,gardens,livingston,fort,greene,morris,park,soho,fresh,meadows,manor,heights,fort,hamilton,morrisania,south,village,glen,oaks,mariner's,harbor,fulton,ferry,mott,haven,stuyvesant,town,glendale,midland,beach,georgetown,mount,eden,sutton,place,hammels,new,brighton,gerritsen,beach,mount,hope,times,square,hillcrest,new,dorp,gowanus,north,riverdale,tribeca,hollis,new,dorp,beach,gravesend,norwood,tudor,city,holliswood,new,springville,greenpoint,olinville,turtle,bay,howard,beach,oakwood,highland,park,parkchester,union,square,hunters,point,old,place,homecrest,pelham,bay,upper,east,side,jackson,heights,old,town,kensington,pelham,gardens,upper,west,side,jamaica,park,hill,kings,highway,pelham,parkway,wall,street,jamaica,center,pleasant,plains,manhattan,beach,port,morris,washington,heights,jamaica,estates,port,ivory,manhattan,terrace,riverdale,west,village,jamaica,hills,port,richmond,mapleton,schuylerville,yorkville,kew,gardens,prince's,bay,marine,park,soundview,kew,gardens,hills,randall,manor,midwood,spuyten,duyvil,laurelton,richmond,town,mill,basin,throgs,neck,lefrak,city,richmond,valley,mill,island,unionport,lindenwood,rosebank,navy,yard,university,heights,little,neck,rossville,new,lots,van,nest,long,island,city,sandy,ground,north,side,wakefield,malba,shore,acres,ocean,hill,west,farms,maspeth,silver,lake,ocean,parkway,westchester,square,middle,village,south,beach,paerdegat,basin,williamsbridge,murray,hill,st.,george,park,slope,woodlawn,neponsit,stapleton,plum,beach,new,hyde,park,sunnyside,prospect,heights,north,corona,todt,hill,prospect,lefferts,gardens,oakland,gardens,tompkinsville,prospect,park,south,ozone,park,tottenville,red,hook,pomonok,travis,remsen,village,queens,village,ward,hill,rugby,queensboro,hill,west,brighton,sea,gate,ravenswood,westerleigh,sheepshead,bay,rego,park,willowbrook,south,side,richmond,hill,woodrow,spring,creek,ridgewood,starrett,city,rochdale,stuyvesant,heights,rockaway,park,sunset,park,rosedale,tompkins,park,north,roxbury,vinegar,hill,seaside,weeksville,somerville,west,brighton,south,corona,williamsburg,south,jamaica,windsor,terrace,south,ozone,park,wingate,springfield,gardens,st.,albans,steinway,sunnyside,sunnyside,gardens,utopia,whitestone,woodhaven,woodside"
street_pattern = "street,st,road,rd,ave,avenue,blvd,drive,court,place,pl,boulevard,way,parkway"
color_ab = "BK,BL,BR,GL,GY,MR,OR,PK,PR,RD,TN,WH,YW,LT,DK,NOCL"

cities = cities.split(",")
cities.sort()
counties = counties.replace("-", " ").split(",")
counties.sort()
borough = borough.split(",")
borough.sort()
borough_ab = borough_ab.split(",")
borough_ab.sort()
school_levels = school_levels.split(",")
school_levels.sort()
park_types = park_types.split(",")
park_types.sort()
colors = colors.split(",")
colors.sort()
business_pattern = business_pattern.split(",")
business_pattern.sort()
school_name_pattern = school_name_pattern.split(",")
school_name_pattern.sort()
neiborhoods = neiborhoods.split(",")
neiborhoods.sort()
street_pattern = street_pattern.split(",")
street_pattern.sort()
color_ab = color_ab.split(",")
color_ab.sort()

def binary_search(source_list, target):
    left = 0
    right = len(source_list) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if source_list[mid] == target:
            return True
        elif source_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def get_type_from_col_name(x):
    col = str(x).lower()
    # Person Name
    if ('first' in col or 'last' in col or 'middle' in col or 'full' in col) and 'name' in col:
        return 'person_name'
    # Business Name
    if ('business' in col and 'name' in col) or 'dba' in col:
        return 'business_name'
    # Phone Number
    if 'phone' in col or 'telephone' in col:
        return 'phone_number'
    # Address
    if 'address' in col:
        return 'address'
    # Street Name
    if 'street' in col:
        return 'street_name'
    # City Agency
    if 'agency' in col:
        return 'city_agency'
    # City
    if 'city' in col and 'agency' not in col:
        return 'city'
    # Neighborhood
    if 'neighborhood' in col:
        return 'neighborhood'
    # LAT/LON coordinates
    if ('lat' in col and 'lon' in col) or 'location' in col:
        return 'lat_lon_cord'
    # Zip code
    if 'zip' in col:
        return 'zip_code'
    # Borough
    if 'boro' in col or 'borough' in col:
        return 'borough'
    # School name
    if col == 'school' or ('school' in col and 'name' in col):
        return 'school_name'
    # Color
    if 'color' in col:
        return 'color'
    # Car Make
    if 'make' in col:
        return 'car_make'
    # Area of study
    if 'interest' in col:
        return 'area_of_study'
    # subjects in school
    if 'subject' in col:
        return 'subject_in_school'
    # school level
    if 'school' in col and 'level' in col:
        return 'school_level'
    # college/university names
    if 'college' in col or 'university' in col:
        return 'college_name'
    # websites
    if 'website' in col or 'site' in col:
        return 'website'
    # building classification
    if 'building' in col and 'classification' in col:
        return 'building_classification'
    # vehicle type
    if 'vehicle' in col and 'type' in col:
        return 'vehicle_type'
    # type of location
    if 'location' in col and 'type' in col:
        return 'location_type'
    # parks/playground
    if 'park' in col and 'name' in col:
        return 'park_playground'
    return 'other'


def check_semantic_type(input):
    predict_types = []
    # check null
    if input is None:
        predict_types.append(('other', 1))
        return predict_types
    x = str(input[0]).strip().lower()
    # Regular Expression
    # Phone Number
    if is_phone(x):
        predict_types.append(('phone_number', input[1]))
    # LAT/LON coordinates
    if is_long_lat(x):
        predict_types.append(('lat_lon_cord', 1))
    # Zip code
    if is_zip(x):
        predict_types.append(('zip_code', input[1]))
    # websites
    if is_website(x):
        predict_types.append(('website', input[1]))
    # External Check (small)
    # School name
    if is_school_name(x):
        predict_types.append(('school_name', input[1]))
    # Borough
    if is_borough(x):
        predict_types.append(('borough', input[1]))
    # school level
    if is_school_level(x):
        predict_types.append(('school_level', input[1]))
    # parks/playground
    if is_park_playground(x):
        predict_types.append(('park_playground', input[1]))
    # Business Name
    if is_business_name(x):
        predict_types.append(('business_name', input[1]))
    # Address
    if is_address(x):
        predict_types.append(('address', input[1]))
    # Street Name
    if is_street(x):
        predict_types.append(('street_name', input[1]))

    # External Check (large)
    # Neighborhood
    if is_neiborhood(x):
        predict_types.append(('neighborhood', input[1]))
    # Color
    if is_color(x):
        predict_types.append(('color', input[1]))
    # City
    if is_city(x):
        predict_types.append(('city', input[1]))
    # Car Make
    # if col_name == 'car_make':
    #     predict_types.append(('car_make', input[1]))
    # City Agency
    # if col_name == 'city_agency':
    #     predict_types.append(('city_agency', input[1]))
    # Area of study

    # subjects in school

    # college/university names

    # building classification
    # vehicle type
    # type of location

    # Final Check
    # Person Name
    # if is_person_name(x):
    #     predict_types.append(('person_name', input[1]))
    if len(predict_types) == 0:
        predict_types.append(('other', input[1]))
    return predict_types


def is_long_lat(x):
    return re.match(
        re.compile(r'^[(]?[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)[)]?$'), x)


def is_school_level(x):
    return binary_search(school_levels, x)


def is_school_name(x):
    x = x.split()
    for e in x:
        if binary_search(school_name_pattern, e):
            return True
    return False


# decide if this string is a street_name or an address
def is_address_helper(x):
    x = x.split()
    int_pattern = re.compile(r'^\d+[-]?\d*$')
    if len(x) >= 3 and re.match(int_pattern, x[0]) and not binary_search(street_pattern, x[1]):
        return True
    else:
        return False


# check if the input string contains a street_name pattern
def is_street_helper(x):
    x = x.split()
    flag = False
    for e in x:
        if e in street_pattern:
            flag = True
            break
    if not flag:
        return False


def is_street(x):
    return is_street_helper(x) and not is_address_helper(x)


def is_address(x):
    return is_street_helper(x) and is_address_helper(x)


def is_color(x):
    return x.lower() in colors


def is_neiborhood(x):
    return binary_search(neiborhoods, x)


def is_zip(x):
    return re.match(re.compile(r'^[\d]{5,5}$'), x)


def is_person_name(x):
    return re.match(
        re.compile(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"), x)


def is_city(x):
    return binary_search(cities, x) or binary_search(counties, x)


def is_park_playground(x):
    # if string x contains any type of park type string, return true, else false
    for e in park_types:
        if e in x:
            return True
    return False


def is_business_name(x):
    # if string x contains any type of business pattern, return true, else false
    for e in business_pattern:
        if e in x:
            return True
    return False


def is_borough(x):
    return binary_search(borough, x) or binary_search(borough_ab, x)


def is_phone(x):
    x = x.replace('(', "").replace(")", "").replace("-", "").replace(" ", "")
    return re.match(re.compile(r'^[\d]{10,10}$'), x)


def is_website(x):
    pattern = re.compile(
        r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}')
    return re.match(pattern, x)


def init_files():
    with open('cluster2.txt') as file:
        origins = [file_name.strip()[1:-1] for file_name in file.readline().split(",")]
    return list(set(origins))


def get_predicted_labels(column_name_type, column_data_type):
    # check if the label is 'other'
    if column_name_type == 'other' and column_data_type[0][0] == 'other':
        return 'other'
    count_total = 0
    count_without_other = 0
    for type in column_data_type:
        count_total += type[1]
        if type[0] != 'other':
            count_without_other += type[1]
    # if count of 'other' is larger than 80%, label this column as 'other'
    # TODO: currently comment for test of other code
    # if count_total - count_without_other >= count_total * 0.8:
    #     return 'other'
    # get all labels with rate of >50% as well as the label from column_name
    res = set()
    res.add(column_name_type)
    for type in column_data_type:
        if type[1] >= count_without_other * 0.5 and type[0] != 'other':
            res.add(type[0])
    return "|".join(list(res))


if __name__ == "__main__":
    sc = SparkContext()
    mkdir("./task2_data")
    data_dir = "/user/hm74/NYCColumns/"
    files = init_files()
    count = 1
    # find column dataset
    result = dict()
    csv_result = []
    for file in files:
        print("-------------------------------------------------------------------------")
        print("file number %s" % count)
        result[file] = dict()
        count += 1
        full_file = data_dir + file
        dataset = file.split(".")[0]
        column = file.split(".")[1]
        print("%s %s start" % (dataset, column))
        # get column type according to name
        column_name_type = get_type_from_col_name(column)
        print(column_name_type)
        file_rdd = sc.textFile(full_file).cache()
        type_rdd = file_rdd.map(lambda x: (x.split("\t")[0], int(x.split("\t")[1]))) \
            .flatMap(check_semantic_type) \
            .reduceByKey(lambda a, b: a + b) \
            .sortBy(lambda x: -x[1]).cache()
        column_data_type = type_rdd.collect()
        result[file]['semantic_types'] = []
        for each_type in column_data_type:
            semantic_types = dict()
            semantic_types['semantic_type'] = each_type[0]
            semantic_types['count'] = each_type[1]
            result[file]['semantic_types'].append(semantic_types)
        predicted_labels = get_predicted_labels(column_name_type, column_data_type)
        csv_result.append(file.replace(".txt.gz", "") + "," + predicted_labels)
        print(column_data_type)
        print(predicted_labels)
    with open("task2.json", 'w+') as fp:
        print("save task2_res.json")
        json.dump(result, fp, cls=MyEncoder)
    with open("predict_label.csv", 'w+') as fp:
        fp.write("column_name,label\n")
        for line in csv_result:
            fp.write(line + "\n")
