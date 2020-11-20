from json import dumps, loads

data_sample = '{"ip_address": "0:12:4b:0:12:5:28:8b", "data": "ax47ay29az-ax18ay69az-64gx-4933gy1003gz1723ax17ay28az-72gx-3740gy-1436gz141ax23ay19az-68gx-4616gy-1060gz973ax33ay11az-68gx-5449gy-414gz8176ax36ay-6az-55gx-5391gy-1501gz588ax36ay-26az-45gx-3945gy-4101gz39ax31ay-62az-51gx-6421gy-6341gz-3ax44ay-46az-65gx-4173gy-7099gz-1ax46ay-34az-63gx211gy-9007gz-151ax54ay-14az-76gx2448gy-9483gz-16ax60ay2az-79gx4278gy-8968gz-1460ax57ay7az-108gx4150gy-6749gz-144ax67ay41az-113gx6641gy-3275gz-14ax44ay47az-101gx2830gy-3250gz-51ax64ay82az-181gx-5847gy2195gz-15ax76ay139az-123gx12538gy11077gz-ax37ay79az-92gx5682gy9564gz1667aax67ay138az-125gx814gy14763gz-68ax41ay131az-64gx-1137gy15203gz10ax33ay95az-85gx-4241gy6067gz6830ax40ay138az-81gx-4993gy11096gz11ax23ay90az-64gx-7903gy6403gz1575ax23ay68az-62gx-2529gy4252gz1289ax30ay72az-51gx-5165gy3663gz1300ax23ay36az-48gx-15195gy607gz1434ax33ay15az-74gx-10732gy-2552gz79ax45ay25az-70gx-12515gy703gz6360ax39ay-5az-63gx-14070gy-924gz510ax51ay-4az-71gx-7757gy-4451gz727ax49ay-15az-63gx-9109gy-3862gz-2ax46ay-33az-57gx-6003gy-5251gz-5ax48ay-47az-79gx-2012gy-7333gz-1ax56ay-21az-81gx257gy-6202gz-178ax63ay12az-74gx6400gy-6192gz-162ax55ay3az-91gx6113gy-6734gz-1342ax53ay22az-103gx5847gy-3663gz-17ax74ay89az-107gx10240gy2227gz-15ax47ay76az-62gx7200gy-404gz-2219ax74ay102az-172gx-6041gy4861gz-1ax61ay159az-79gx7916gy12974gz433ax55ay117az-113gx2448gy11335gz-1ax68ay190az-68gx6368gy16947gz252ax25ay98az-56gx-10461gy5165gz194ax38ay82az-111gx-10248gy4636gz13ax27ay98az-42gx-213gy11198gz1193ax27ay77az-53gx-13098gy4287gz116ax30ay59az-59gx-6606gy5553gz9538ax34ay74az-28gx-4550gy4515gz5376ax35ay50az-38gx-15319gy-1479gz67ax39ay26az-54gx-13012gy-2924gz51ax45ay21az-51gx-6618gy-3432gz-15ax49ay17az-49gx-5725gy-3998gz-41ax59ay35az-49gx-1578gy-6954gz-81ax62ay2az-66gx-5016gy-10283gz-53ax66ay-12az-83gx-2703gy-8320gz-1ax83ay21az-68gx7706gy-7911gz-105ax70ay-23az-66gx4589gy-7438gz-66ax57ay-23az-84gx4348gy-7856gz-19ax77ay36az-97gx10583gy-4562gz-16ax57ay30az-90gx6731gy-1630gz-126ax55ay62az-96gx7977gy2070gz-1365ax42ay82az-82gx5868gy4301gz-4630ax57ay102az-115gx5017gy2491gz-28ax44ay94az-119gx4158gy5960gz2202ax44ay117az-113gx9893gy11558gz-5ax48ay163az-91gx-465gy10051gz293ax45ay137az-118gx-3341gy10577gz3ax41ay149az-91gx-2552gy11319gz92ax26ay111az-71gx-8892gy9410gz119ax24ay97az-63gx-8354gy7541gz1233ax26ay83az-65gx-7811gy6606gz1277ax23ay69az-47gx-10764gy4301gz119ax27ay49az-55gx-12772gy1577gz121ax31ay29az-53gx-10351gy210gz9245ax42ay32az-48gx-7609gy-1674gz574ax48ay25az-49gx-8351gy-3065gz411ax55ay20az-55gx-9175gy-5240gz304ax56ay-2az-57gx-7236gy-6253gz212ax54ay-22az-58gx-4344gy-7041gz-2ax50ay-40az-54gx-1368gy-9841gz-1ax45ay-43az-74gx192gy-10015gz-17ax47ay-15az-86gx4864gy-7949gz-24ax47ay10az-106gx9480gy-6206gz-25ax69ay60az-104gx13785gy-41gz-250ax48ay49az-77gx12185gy3116gz-164ax38ay58az-98gx5104gy2767gz-1907ax47ay108az-88gx12254gy8274gz-92ax10ay65az-71gx-2750gy2995gz-535ax11ay114az-110gx14894gy8649gz-4ax-6ay126az-86gx-2309gy-425gz-87ax54ay199az-200gx-1592gy6105gz-3ax-6ay113az-124gx325gy12906gz115ax18ay153az-85gx2612gy11500gz573ax5ay153az-58gx-13287gy7494gz180ax-3ay95az-98gx-14291gy3258gz202ax5ay92az-76gx-995gy6190gz17440aax5ay57az-64gx-5661gy3353gz19290ax12ay30az-58gx-4940gy938gz18747ax15ay-12az-51gx-5980gy-1227gz16ax18ay-33az-46gx-5706gy-1747gz81ax26ay-23az-59gx-10014gy-2363gz-ax54ay25az-63gx-2135gy-3016gz-32ax50ay13az-38gx-3974gy-7135gz300ax45ay-37az-65gx-6518gy-8298gz-9ax49ay-31az-73gx-6374gy-7950gz-1ax68ay14az-90gx1238gy-9005gz-136ax76ay21az-91gx3791gy-8358gz-823ax66ay5az-86gx4000gy-6361gz-6545ax56ay5az-92gx4798gy-5275gz-7041ax46ay17az-118gx1390gy-4148gz-96ax59ay69az-143gx2704gy4479gz-124ax52ay80az-125gx5681gy5003gz-836ax48ay95az-150gx3152gy11925gz-13ax52ay172az-66gx7722gy18273gz-54ax58ay135az-94gx-8371gy7193gz349ax51ay118az-100gx-6gy13716gz3828ax50ay148az-61gx-5739gy13382gz10ax23ay89az-75gx-8008gy9535gz1503ax21ay92az-53gx-2219gy10919gz103ax21ay90az-31gx-7801gy6426gz1205ax28ay68az-45gx-13044gy1987gz134ax28ay25az-44gx-11810gy-1138gz10ax33ay11az-49gx-11164gy-2541gz52ax55ay42az-49gx-7422gy-4524gz454ax48ay9az-47gx-7925gy-7188gz5191ax54ay4az-53gx-6440gy-8712gz3829ax68ay31az-75gx-2590gy-7847gz-24ax71ay32az-52gx-3203gy-10036gz66ax51ay-44az-79gx-10898gy-10513gzax49ay-41az-62gx-2740gy-9719gz-4ax68ay-22az-84gx-2635gy-12371gz-ax48ay-43az-85gx-1706gy-10521gz-ax77ay25az-108gx-945gy-3903gz-15ax70ay37az-76gx1381gy-2321gz-105ax53ay-4az-99gx-3192gy-6400gz-41ax35ay-8az-132gx7267gy-2469gz-13ax39ay71az-110gx9538gy4028gz-175ax49ay86az-144gx-1822gy4782gz-10ax51ay109az-156gx6169gy10040gz-1ax58ay148az-100gx4842gy14872gz-5ax46ay110az-115gx1821gy13839gz-1ax46ay135az-75gx5045gy16819gz392ax44ay125az-73gx-529gy12552gz639ax37ay104az-58gx-25gy11753gz8232ax39ay108az-42gx-2726gy12200gz89ax38ay104az-35gx-2803gy4754gz145ax32ay81az-47gx-4334gy2074gz1718ax37ay58az-68gx-2603gy-275gz1684ax33ay63az-22gx10172gy-2851gz233ax17ay0az-44gx-4189gy-5041gz2315ax22ay-46az-75gx-5164gy-2355gz15ax28ay-44az-57gx-1369gy-2122gz69ax41ay-28az-43gx-4270gy-3469gz89ax31ay-66az-48gx-6176gy-4416gz65ax30ay-77az-46gx-7291gy-4211gz98ax35ay-7"}'
d = loads(data_sample)
print(d['ip_address'])
print(d['data'])