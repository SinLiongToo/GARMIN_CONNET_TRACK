// =======================================================================
// 🩹 200 Clinical Running Injury & Biomechanics Sentences Database
// 200 句路跑運動傷害、生物力學預防、臨床診斷與運動醫學雙語例句資料庫
// =======================================================================

const RUNNING_INJURY_SENTENCES = [
  {
    "id": 1,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Iliotibial Band Syndrome (ITBS)",
    "en": "Weak hip abductors and excessive pelvic drop allow the iliotibial band to repeatedly rub against the lateral femoral epicondyle, provoking sharp lateral knee pain during foot strike.",
    "zh": "臀部外展肌群無力與骨盆過度下傾會導致髂脛束反覆摩擦股骨外上髁，在著地瞬間引發膝蓋外側銳利刺痛。",
    "tag": "#ITBS"
  },
  {
    "id": 2,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Patellofemoral Pain Syndrome (PFPS)",
    "en": "Patellofemoral pain syndrome typically stems from quadriceps muscle imbalances that cause abnormal lateral tracking of the patella within the femoral trochlear groove.",
    "zh": "髕骨股骨疼痛症候群通常源自股四頭肌肌力失衡，導致髕骨在股骨滑車溝內出現異常的外側滑移軌跡。",
    "tag": "#RunnerKnee"
  },
  {
    "id": 3,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Patellar Tendinopathy (Jumper's Knee)",
    "en": "Repetitive high-impact deceleration and downhill bounding can induce micro-tears in the patellar tendon, causing point tenderness directly at the inferior pole of the patella.",
    "zh": "反覆的高衝擊減速與下坡跳躍會誘發髕骨肌腱微撕裂，在髕骨下極邊緣產生明確的定點壓痛。",
    "tag": "#PatellarTendon"
  },
  {
    "id": 4,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Pes Anserine Bursitis",
    "en": "Friction between the conjoined tendon of the sartorius, gracilis, and semitendinosus and the medial tibia causes pes anserine bursitis, presenting as burning pain two inches below the medial joint line.",
    "zh": "縫匠肌、股薄肌與半腱肌的聯合肌腱與脛骨內側反覆摩擦會誘發鵝足滑囊炎，在內側關節線下方兩英吋處表現為灼熱隱痛。",
    "tag": "#PesAnserine"
  },
  {
    "id": 5,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Popliteus Tendinopathy",
    "en": "The popliteus muscle acts as the primary dynamic stabilizer preventing anterior femoral translation during steep trail descents, making it highly susceptible to eccentric overload.",
    "zh": "膕肌是防止陡峭越野下坡時股骨向前滑動的主要動態穩定器，因而極易承受過度的離心負荷而受損。",
    "tag": "#PopliteusTendon"
  },
  {
    "id": 6,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Chondromalacia Patellae",
    "en": "Softening and progressive fibrillation of the retro-patellar articular cartilage generates a grinding crepitus sensation when ascending stairs or rising from a deep squat.",
    "zh": "髕骨後方關節軟骨的軟化與退化性原纖維化，會在爬樓梯或從深蹲起身時產生明顯的關節摩擦沙沙聲。",
    "tag": "#Chondromalacia"
  },
  {
    "id": 7,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Medial Meniscal Posterior Horn Tear",
    "en": "Deep rotational twisting under axial weight-bearing can tear the posterior horn of the medial meniscus, producing a sharp catching sensation and joint line effusion.",
    "zh": "軸向承重下的深層旋轉扭轉可能撕裂內側半月板後角，引發關節卡鎖交鎖感與關節腔積液腫脹。",
    "tag": "#MeniscusTear"
  },
  {
    "id": 8,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Hoffa's Fat Pad Impingement",
    "en": "Genu recurvatum or repetitive knee hyperextension pinches the richly innervated infrapatellar fat pad between the patellar tendon and femoral condyle, triggering sharp anterior pain.",
    "zh": "膝關節過度反折超伸會將神經密布的髕下脂肪墊夾擠在髕腱與股骨髁之間，觸發劇烈的前膝深層刺痛。",
    "tag": "#HoffasFatPad"
  },
  {
    "id": 9,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Synovial Plica Syndrome",
    "en": "An inflamed embryonic synovial fold known as a medio-patellar plica can snap tautly over the medial femoral condyle, mimicking a torn medial meniscus.",
    "zh": "稱為髕骨內側皺襞的發炎性胚胎滑膜皺褶會在內側股骨髁上緊繃彈響，其症狀常高度模擬內側半月板撕裂。",
    "tag": "#PlicaSyndrome"
  },
  {
    "id": 10,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Biceps Femoris Insertional Tendinopathy",
    "en": "Excessive toe-out running form increases lateral rotational strain on the distal insertion of the biceps femoris tendon at the fibular head.",
    "zh": "過度外八字的跑步步態會顯著增加股二頭肌肌腱在腓骨頭遠端附著處的外側旋轉牽拉張力。",
    "tag": "#BicepsFemoris"
  },
  {
    "id": 11,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Knee Joint Effusion",
    "en": "Intra-articular fluid accumulation within the suprapatellar pouch indicates acute capsule irritation or cartilage micro-trauma, dramatically inhibiting quadriceps firing.",
    "zh": "髕上囊內關節液的異常積聚預示著急性關節囊刺激或軟骨微創傷，並會反射性劇烈抑制股四頭肌的神經徵召。",
    "tag": "#KneeEffusion"
  },
  {
    "id": 12,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Cadence and Knee Impact Reduction",
    "en": "Increasing running cadence by 5 to 10 percent reduces the peak knee flexion angle and diminishes patellofemoral joint contact forces by up to 20 percent.",
    "zh": "將跑步步頻提高百分之五至十可減小峰值膝關節屈曲角度，並將髕骨股骨關節接觸衝擊力降低高達百分之二十。",
    "tag": "#CadenceReduction"
  },
  {
    "id": 13,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Overstriding Knee Shear",
    "en": "Landing with the foot far ahead of the body's center of mass generates excessive braking shear forces that travel directly through the extended knee joint.",
    "zh": "著地點遠超身體重心的過度跨步會產生巨大的制動剪切力，並直接穿透伸直鎖定的膝關節造成傷害。",
    "tag": "#OverstridingKnee"
  },
  {
    "id": 14,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Dynamic Knee Valgus Collapse",
    "en": "Dynamic knee valgus collapse during single-leg stance places tremendous tensile strain on the medial collateral ligament and lateral joint compartment compression.",
    "zh": "單腿支撐期的動態膝外翻塌陷會對內側副韌帶施加巨大的拉伸張力，同時造成外側關節腔的壓縮磨損。",
    "tag": "#DynamicValgus"
  },
  {
    "id": 15,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Quadriceps Tendinopathy",
    "en": "Pain localized just superior to the base of the patella reflects quadriceps tendinopathy, often exacerbated by explosive track sprints and plyometric jump training.",
    "zh": "局限於髕骨上緣基底部的疼痛反映出股四頭肌腱病變，這種損傷常因高爆發力間歇衝刺與增強式跳躍訓練而加劇。",
    "tag": "#QuadTendinopathy"
  },
  {
    "id": 16,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Iliotibial Band Bursa Friction",
    "en": "Repetitive knee flexion and extension cycles between 20 and 30 degrees create maximal impingement of the richly vascularized tissue beneath the distal iliotibial band.",
    "zh": "膝關節在屈曲二十至三十度之間的重複往復擺動，會對遠端髂脛束深層富含血管的組織造成最大程度的擠壓摩擦。",
    "tag": "#ITBImpingement"
  },
  {
    "id": 17,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Lateral Collateral Ligament Strain",
    "en": "Running on crowned or banked asphalt roads forces the uphill leg into varus alignment, predisposing the lateral collateral ligament to chronic micro-strains.",
    "zh": "在傾斜拱形的柏油路面奔跑會迫使上坡側腿部呈現內翻力線，使外側副韌帶長期承受微小拉傷的累積風險。",
    "tag": "#LCLStrain"
  },
  {
    "id": 18,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Anterior Cruciate Ligament Micro-Stress",
    "en": "High deceleration forces combined with knee internal rotation and foot pronation significantly elevate baseline ligamentous strain across the anterior cruciate ligament.",
    "zh": "強烈的減速力結合膝關節內旋與足部過度旋前，會大幅抬升前十字韌帶的基線拉伸張力負荷。",
    "tag": "#ACLStress"
  },
  {
    "id": 19,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Vastus Medialis Oblique (VMO) Atrophy",
    "en": "Selective disuse atrophy of the vastus medialis oblique allows the stronger lateral quadriceps to displace the patella laterally during terminal knee extension.",
    "zh": "股內側肌的選擇性廢用萎縮會使力量較強的外側肌群在伸膝末期將髕骨向外側牽引偏離正常滑軌。",
    "tag": "#VMOWeakness"
  },
  {
    "id": 20,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Knee Joint Hyperextension Recurvatum",
    "en": "Allowing the knee joint to snap into hyperextension at push-off stresses the posterior joint capsule and squashes the posterior horn of the lateral meniscus.",
    "zh": "蹬地推蹬瞬間若放任膝關節猛烈反折超伸，會拉扯後關節囊並劇烈擠壓外側半月板後角。",
    "tag": "#KneeRecurvatum"
  },
  {
    "id": 21,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Quadriceps Angle (Q-Angle) Influence",
    "en": "A wide anatomical Q-angle increases the lateral vector force acting on the patella, predisposing female endurance runners to patellofemoral pain syndrome.",
    "zh": "較寬的解剖 Q 角會顯著增加作用於髕骨上的外向向量合力，使女性耐力跑者更容易罹患髕骨股骨疼痛症候群。",
    "tag": "#QAngleBiomechanics"
  },
  {
    "id": 22,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Hamstring-to-Quadriceps Strength Ratio",
    "en": "A hamstring-to-quadriceps isometric strength ratio below 0.6 compromises knee joint stability during high-speed downhill running intervals.",
    "zh": "膕繩肌與股四頭肌等長肌力比值若低於零點六，會在高速下坡跑間歇中嚴重損害膝關節的動態抗衝擊穩定性。",
    "tag": "#HQRatio"
  },
  {
    "id": 23,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Articular Cartilage Micro-Fissuring",
    "en": "Repetitive compressive impact exceeding chondrocyte repair capacity triggers superficial cartilage micro-fissuring, predisposing runners to early osteoarthritis.",
    "zh": "超過軟骨細胞修復能力的重複壓縮衝擊會觸發淺層軟骨微裂痕，增加跑者過早發生退化性骨關節炎的機率。",
    "tag": "#CartilageFissuring"
  },
  {
    "id": 24,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Prepatellar Bursitis (Housemaid's Knee)",
    "en": "Direct blunt trauma from falling onto rocky trail terrain can induce acute prepatellar bursitis, swelling the subcutaneous space anterior to the kneecap.",
    "zh": "在碎石越野山徑上跌倒直接撞擊地面會誘發急性髕前滑囊炎，使髕骨前方的皮下空間迅速膨脹積液。",
    "tag": "#PrepatellarBursitis"
  },
  {
    "id": 25,
    "cat_id": "knee",
    "cat_zh": "膝關節與髕骨",
    "injury": "Knee Extension Lag",
    "en": "An inability to achieve full active knee extension despite complete passive mobility indicates quadriceps inhibition triggered by knee joint pain or swelling.",
    "zh": "在具備完整被動活動度的情況下無法主動完全伸直膝關節，代表膝關節疼痛或腫脹已引發股四頭肌神經抑制。",
    "tag": "#ExtensionLag"
  },
  {
    "id": 26,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Plantar Fasciitis",
    "en": "Morning first-step heel pain occurs because the micro-tears sustained by the plantar fascia during yesterday's long run attempt to heal in a shortened position overnight.",
    "zh": "早晨下床第一步的足跟刺痛，是因為昨日長跑累積的足底筋膜微撕裂在夜間處於縮短位置自癒所致。",
    "tag": "#PlantarFasciitis"
  },
  {
    "id": 27,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Windlass Mechanism Failure",
    "en": "Restricted great toe extension impairs the windlass mechanism, preventing the plantar fascia from tightening and locking the tarsal bones into a rigid propulsive lever.",
    "zh": "大腳趾背屈活動度受限會破壞風車蓄能機制，阻礙足底筋膜緊繃並使足跗骨無法鎖定為剛性推進槓桿。",
    "tag": "#WindlassMechanism"
  },
  {
    "id": 28,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Morton's Neuroma",
    "en": "Tight, narrow-fitting running shoes squeeze the transverse metatarsal arch, causing chronic irritation and fibrous thickening of the third interdigital plantar nerve.",
    "zh": "緊繃且狹窄的跑鞋鞋楦會擠壓前足橫弓，導致第三趾間足底神經受到長期慢性刺激並增生纖維化腫塊。",
    "tag": "#MortonsNeuroma"
  },
  {
    "id": 29,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Great Toe Sesamoiditis",
    "en": "The two pea-sized sesamoid bones embedded within the flexor hallucis brevis tendon absorb massive forefoot impact and can become severely inflamed during hill sprints.",
    "zh": "內嵌於屈拇短肌腱內的兩顆豌豆大小種子骨承載著巨大的前足衝擊，在坡道衝刺時極易引發嚴重的種子骨炎。",
    "tag": "#Sesamoiditis"
  },
  {
    "id": 30,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Medial Longitudinal Arch Collapse",
    "en": "Progressive weakness of the intrinsic foot musculature leads to medial longitudinal arch collapse, overloading the plantar fascia and increasing tibial internal rotation.",
    "zh": "足底內在肌群的進行性無力會導致內側縱足弓塌陷，使足底筋膜超負荷過載並劇烈增加脛骨內旋代償。",
    "tag": "#ArchCollapse"
  },
  {
    "id": 31,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Subungual Hematoma (Black Toenail)",
    "en": "Repetitive mechanical shearing from the toes slamming against the shoe toe-box during marathons ruptures capillary vessels under the nail plate, causing a throbbing black toenail.",
    "zh": "在馬拉松過程中腳趾反覆猛烈頂撞鞋頭產生的機械剪力會震破甲床微血管，造成劇烈搏動脹痛的黑指甲。",
    "tag": "#BlackToenail"
  },
  {
    "id": 32,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Metatarsalgia",
    "en": "Excessive plantar pressures concentrated beneath the second and third metatarsal heads during forefoot striking cause chronic inflammatory aching known as metatarsalgia.",
    "zh": "前足著地時過度集中的足底壓力施加於第二與第三蹠骨頭下方，會引發稱為蹠骨痛的慢性發炎性酸痛。",
    "tag": "#Metatarsalgia"
  },
  {
    "id": 33,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Plantar Fascia Rupture",
    "en": "A sudden audible pop accompanied by intense mid-foot pain during explosive hill acceleration indicates an acute partial or complete tear of the central plantar aponeurosis.",
    "zh": "在坡道爆發加速時若伴隨清脆的啪裂聲與足弓中段劇痛，代表中央足底腱膜已發生急性部分或完全撕裂。",
    "tag": "#FasciaRupture"
  },
  {
    "id": 34,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Abductor Hallucis Muscle Atrophy",
    "en": "Atrophy of the abductor hallucis muscle impairs dynamic stabilization of the first ray, predisposing distance runners to bunion formation and medial foot fatigue.",
    "zh": "外展拇肌的萎縮會損害第一足射線的動態穩定度，使長跑跑者更容易形成拇指外翻與內側足部疲勞。",
    "tag": "#AbductorHallucis"
  },
  {
    "id": 35,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Friction Blister Formation",
    "en": "Frictional shear forces between the stratum corneum and deeper epidermal layers trigger intra-epidermal fluid cleavage, forming painful fluid-filled blisters on long trail runs.",
    "zh": "角質層與表皮深層之間的摩擦剪切力會誘發表皮內裂開積液，在長途越野奔跑中形成充滿組織液的劇痛水泡。",
    "tag": "#FrictionBlisters"
  },
  {
    "id": 36,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Tarsal Tunnel Syndrome",
    "en": "Compression of the posterior tibial nerve as it travels through the fibro-osseous tarsal tunnel behind the medial malleolus causes burning numbness across the bottom of the foot.",
    "zh": "脛後神經在通過內踝後方的纖維骨性跗骨隧道時受到擠壓，會導致足底蔓延灼熱麻木感。",
    "tag": "#TarsalTunnel"
  },
  {
    "id": 37,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Fat Pad Atrophy of the Heel",
    "en": "Age-related thinning or trauma-induced degeneration of the specialized shock-absorbing calcaneal fat pad diminishes natural cushioning, resulting in deep bone bruising under the heel.",
    "zh": "隨著年齡老化或外傷導致跟骨特化減震脂肪墊變薄退化，會大幅削弱天然緩衝能力，引發足跟深層骨挫傷。",
    "tag": "#FatPadAtrophy"
  },
  {
    "id": 38,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Turf Toe (First MTP Joint Sprain)",
    "en": "Forceful hyperextension of the first metatarsophalangeal joint sprains the plantar capsular ligamentous complex, crippling the runner's ability to push off the big toe.",
    "zh": "第一蹠趾關節的猛烈過度背屈會拉傷足底關節囊韌帶複合體，嚴重癱瘓跑者利用大腳趾蹬地推蹬的能力。",
    "tag": "#TurfToe"
  },
  {
    "id": 39,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Navicular Stress Injury",
    "en": "The central one-third of the tarsal navicular bone possesses an avascular zone, rendering it exceptionally vulnerable to debilitating stress reactions under high running mileage.",
    "zh": "足跗舟狀骨中央三分之一區域缺乏血管供應，使其在高跑量衝擊下極易發生令人衰竭的應力反應甚至骨折。",
    "tag": "#NavicularStress"
  },
  {
    "id": 40,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Extensor Tendinitis of the Foot",
    "en": "Lacing your running shoes too tightly over the instep pinches the extensor digitorum and hallucis longus tendons against the tarsal bones, causing crepitus and dorsal aching.",
    "zh": "在腳背上將鞋帶繫得過緊會將趾長伸肌與拇長伸肌腱夾擠在跗骨上，造成腳背彈響雜音與酸痛。",
    "tag": "#ExtensorTendinitis"
  },
  {
    "id": 41,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Plantar Fibromatosis (Ledderhose Disease)",
    "en": "Slow-growing, benign fibrous nodules embedded within the deep plantar fascia band can become exquisitely tender when compressed directly against firm running shoe insoles.",
    "zh": "深植於足底筋膜深處生長緩慢的良性纖維結節，在與堅硬跑鞋鞋墊直接擠壓時會產生劇烈的壓痛感。",
    "tag": "#PlantarFibroma"
  },
  {
    "id": 42,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Tailor's Bunion (Bunionette)",
    "en": "Lateral deviation of the fifth metatarsal head causes painful friction and bursa swelling against the outer side of the running shoe upper.",
    "zh": "第五蹠骨頭的外側偏斜會在與跑鞋鞋面外側反覆摩擦時引發劇烈疼痛與滑囊腫脹。",
    "tag": "#TailorsBunion"
  },
  {
    "id": 43,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Spring Ligament Complex Strain",
    "en": "Tearing of the plantar calcaneonavicular spring ligament complex compromises passive arch support, causing dynamic hyperpronation and severe midfoot strain.",
    "zh": "足底跟舟足弓韌帶（彈簧韌帶）複合體的撕裂會摧毀被動足弓支撐，引發動態過度內旋與嚴重的足中段拉傷。",
    "tag": "#SpringLigament"
  },
  {
    "id": 44,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Cuboid Syndrome",
    "en": "Disruption of the calcaneocuboid joint following an inversion ankle sprain can cause the cuboid bone to subluxate downward, creating pinpoint lateral midfoot agony.",
    "zh": "腳踝內翻扭傷後跟骰關節結構被打亂可能使骰骨向下半脫位，在前足外側中段造成針尖般的定點劇痛。",
    "tag": "#CuboidSyndrome"
  },
  {
    "id": 45,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Carbon Plate Forefoot Metatarsal Load",
    "en": "Extremely rigid full-length carbon-fiber plates alter natural toe metatarsophalangeal articulation, shifting high peak bending moments onto the metatarsal shafts.",
    "zh": "剛性極高的全掌碳纖維板改變了自然的腳趾蹠趾關節活動度，將極高的峰值彎矩轉移並集中至蹠骨幹上。",
    "tag": "#CarbonPlateLoad"
  },
  {
    "id": 46,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Zero-Drop Transition Calf-Plantar Strain",
    "en": "Transitioning abruptly from a 10mm drop shoe to a zero-drop minimalist shoe places sudden eccentric stretch on the Achilles tendon and doubles tensile load on the plantar fascia.",
    "zh": "從十毫米落差鞋驟然切換至零落差極簡鞋，會對阿基里斯腱施加突如其來的離心伸展，使足底筋膜拉伸負荷倍增。",
    "tag": "#ZeroDropTransition"
  },
  {
    "id": 47,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Dorsal Foot Nerve Entrapment",
    "en": "The superficial peroneal nerve branch crossing the dorsal midfoot can be trapped beneath rigid tongue overlays, generating shooting numbness into the middle toes.",
    "zh": "跨越腳背中段的腓淺神經皮下分支若被僵硬的鞋舌外飾壓迫，會在中間腳趾引發放射性的麻木刺痛。",
    "tag": "#DorsalNerveEntrapment"
  },
  {
    "id": 48,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Heel Spur Friction Myth",
    "en": "Research demonstrates that subcalcaneal bone spurs are often asymptomatic incidental findings, with real heel pain originating from micro-tears within the plantar fascia insertion.",
    "zh": "運動醫學研究證實足跟骨刺通常是無症狀的伴隨發現，真正的足跟劇痛實質源自足底筋膜附著處的微撕裂與神經發炎。",
    "tag": "#HeelSpurFact"
  },
  {
    "id": 49,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Foot Arch Stiffness Adaptation",
    "en": "A rigid high-arched foot acts as a poor shock absorber, transferring ground reaction forces upward to cause stress fractures and lateral knee pain.",
    "zh": "僵硬的高足弓天然減震緩衝能力極差，會將地面反作用力未經吸收直接向上传導，誘發疲勞性骨折與膝蓋外側痛。",
    "tag": "#HighArchStiffness"
  },
  {
    "id": 50,
    "cat_id": "foot",
    "cat_zh": "足底與足弓",
    "injury": "Plantar Fascia Ultrasound Thickness",
    "en": "Ultrasound diagnostic imaging revealing a plantar fascia thickness exceeding 4.0 millimeters directly confirms chronic plantar fasciopathy and collagen degeneration.",
    "zh": "超音波診斷影像若顯示足底筋膜厚度超過四點零毫米，即可直接確診為慢性足底筋膜病變伴隨膠原蛋白退化變性。",
    "tag": "#FasciaUltrasound"
  },
  {
    "id": 51,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Mid-Portion Achilles Tendinopathy",
    "en": "Pain and morning stiffness localized 2 to 6 centimeters above the calcaneal insertion characterises mid-portion Achilles tendinopathy, driven by failed collagen healing.",
    "zh": "局限於跟骨附著點上方二至六公分處的疼痛與晨間僵硬是阿基里斯腱中段病變的特徵，由膠原修復衰竭所驅動。",
    "tag": "#AchillesMidPortion"
  },
  {
    "id": 52,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Insertional Achilles Tendinopathy",
    "en": "Direct insertional Achilles tendinopathy causes pain right on the posterior calcaneus and is severely aggravated by dorsiflexion stretches over the edge of stairs.",
    "zh": "附著點型阿基里斯腱病變在跟骨後側直接產生劇痛，並會因在樓梯邊緣過度被動背屈拉伸而顯著惡化。",
    "tag": "#InsertionalAchilles"
  },
  {
    "id": 53,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Alfredson Eccentric Heel Drop Protocol",
    "en": "Performing 180 daily eccentric heel drops with straight and bent knees across twelve weeks stimulates tendon remodeling and realigns disorganized type I collagen fibers.",
    "zh": "在十二週內每天以直膝與屈膝姿態進行一百八十次離心降跟提踵訓練，能刺激肌腱重塑並重新排列雜亂的第一型膠原纖維。",
    "tag": "#AlfredsonProtocol"
  },
  {
    "id": 54,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Heavy Slow Resistance (HSR) Training",
    "en": "Heavy slow resistance training utilizing 3-second concentric and 3-second eccentric tempos promotes superior tendon mechanical stiffness compared to passive stretching.",
    "zh": "採用三秒向心與三秒離心節奏的高負重慢速阻力訓練，比單純被動拉伸更能顯著提升肌腱的機械剛性與儲能能力。",
    "tag": "#HSRTraining"
  },
  {
    "id": 55,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Retrocalcaneal Bursitis",
    "en": "Inflammation of the fluid-filled retrocalcaneal bursa located between the Achilles tendon and the anterior-superior surface of the calcaneus causes deep retro-heel throbbing.",
    "zh": "位於阿基里斯腱與跟骨前上方骨面之間的跟骨後滑囊發炎，會在足跟深處引發持續跳動的搏動性脹痛。",
    "tag": "#RetrocalcanealBursa"
  },
  {
    "id": 56,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Haglund's Deformity (Pump Bump)",
    "en": "A prominent bony enlargement on the posterosuperior aspect of the calcaneus known as Haglund's deformity chronically pinches the Achilles tendon against stiff heel counters.",
    "zh": "稱為哈格蘭德畸形（Haglund 骨刺）的跟骨後上方骨性凸起，會在堅硬的跑鞋後跟杯內長期夾擠摩擦阿基里斯腱。",
    "tag": "#HaglundsDeformity"
  },
  {
    "id": 57,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Peroneal Retinaculum Tear and Subluxation",
    "en": "Rupture of the superior peroneal retinaculum allows the peroneal tendons to pop out of their groove and snap forward over the lateral malleolus during fast trail corners.",
    "zh": "上腓骨肌支持帶破裂會使腓骨長短肌腱脫出骨槽，並在快速越野過彎時向前彈跳滑過外踝骨突引發劇痛。",
    "tag": "#PeronealSubluxation"
  },
  {
    "id": 58,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Anterior Talofibular Ligament (ATFL) Sprain",
    "en": "Landing unexpectedly on an exposed tree root forces the ankle into sudden inversion and plantarflexion, tearing the anterior talofibular ligament.",
    "zh": "著地時若不慎踩踏在裸露的樹根上會迫使腳踝猛烈內翻伴隨蹠屈，直接撕裂外踝的前距腓韌帶。",
    "tag": "#ATFLSprain"
  },
  {
    "id": 59,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Calcaneofibular Ligament (CFL) Tear",
    "en": "Severe grade-two and grade-three ankle inversion trauma extends beyond the ATFL to compromise the calcaneofibular ligament, creating extensive lateral ecchymosis.",
    "zh": "嚴重的二級與三級腳踝內翻扭傷會自前距腓韌帶延伸並撕裂跟腓韌帶，造成足部外側廣泛的皮下大片瘀血。",
    "tag": "#CFLTear"
  },
  {
    "id": 60,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "High Ankle Sprain (Syndesmotic Injury)",
    "en": "Forceful external rotation of the talus while the ankle is dorsiflexed separates the distal tibia and fibula, tearing the anterior inferior tibiofibular syndesmosis.",
    "zh": "當腳踝處於背屈狀態時距骨受到強烈的外旋扭轉，會撐開遠端脛腓骨並撕裂下脛腓前韌帶聯合結構（高位扭傷）。",
    "tag": "#HighAnkleSprain"
  },
  {
    "id": 61,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Posterior Tibial Tendon Dysfunction (PTTD)",
    "en": "Failure of the posterior tibial tendon allows the talar head to drop inferomedially, extinguishing push-off power and causing secondary compression under the lateral malleolus.",
    "zh": "脛後肌腱功能衰竭會使距骨頭向內下方塌陷墜落，不僅徹底瓦解蹬地推蹬力量，還會在距骨外翻時引發外踝下方次級夾擠痛。",
    "tag": "#PTTDFailure"
  },
  {
    "id": 62,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Anterior Ankle Impingement",
    "en": "Repetitive maximal dorsiflexion in uphill trail running creates micro-trauma along the anterior rim of the tibia, developing bony spurs that pinch the ankle capsule.",
    "zh": "上坡越野跑中反覆達到極限的踝背屈會在脛骨前緣累積微創傷，逐漸增生骨刺並夾擠前關節囊引發刺痛。",
    "tag": "#AnteriorImpingement"
  },
  {
    "id": 63,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Posterior Ankle Impingement (Os Trigonum)",
    "en": "Forced plantarflexion during sprinting pinches an accessory ossicle known as the os trigonum between the posterior talus and calcaneus, causing deep posterior ankle pain.",
    "zh": "衝刺跑時強烈的足部蹠屈會將稱為三角骨的副骨夾擠在距骨後突與跟骨之間，引發足踝後方深層的卡夾性劇痛。",
    "tag": "#OsTrigonum"
  },
  {
    "id": 64,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Achilles Tendon Rupture",
    "en": "A catastrophic sensation like being kicked violently in the back of the ankle followed by an inability to perform a single-leg heel raise denotes an acute Achilles rupture.",
    "zh": "腳踝後方突然感受到如同被重物猛烈踢擊的劇烈衝擊，隨後完全無法進行單腿提踵，預示著阿基里斯腱已發生急性完全斷裂。",
    "tag": "#AchillesRupture"
  },
  {
    "id": 65,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Peroneal Tendinopathy",
    "en": "Chronic tendon thickening and crepitus along the lateral ankle border below the fibular tip indicates peroneal tendinopathy, often exacerbated by excessive foot supination.",
    "zh": "外踝下緣沿著腳踝外側邊緣出現的慢性肌腱增厚與沙沙彈響，是腓骨肌腱病變的表徵，常因足部過度旋後而惡化。",
    "tag": "#PeronealTendinitis"
  },
  {
    "id": 66,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Flexor Hallucis Longus (FHL) Tendinopathy",
    "en": "Running dancers and steep hill runners frequently irritate the flexor hallucis longus tendon as it traverses the fibro-osseous groove behind the medial malleolus.",
    "zh": "舞蹈跑者與陡坡越野跑者常在拇長屈肌腱通過內踝後方纖維骨溝處引發腱鞘發炎與大腳趾活動受限。",
    "tag": "#FHLTendinopathy"
  },
  {
    "id": 67,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Subtalar Joint Instability",
    "en": "Repetitive ankle sprains damage the interosseous talocalcaneal ligament, resulting in subtalar joint hypermobility that undermines balance over technical scree fields.",
    "zh": "反覆的腳踝扭傷會破壞距跟骨間韌帶，引發距下關節微失穩，嚴重削弱在崎嶇碎石坡面上的動態平衡能力。",
    "tag": "#SubtalarInstability"
  },
  {
    "id": 68,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Ankle Dorsiflexion Restriction",
    "en": "A weight-bearing lunge test revealing less than 10 centimeters of knee-to-wall distance denotes severe ankle dorsiflexion restriction that forces compensatory midfoot collapse.",
    "zh": "負重弓步膝碰牆測試若小於十公分，代表踝關節背屈活動度嚴重受限，將迫使足中段以過度塌陷內旋進行代償。",
    "tag": "#DorsiflexionLimit"
  },
  {
    "id": 69,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Tendon Neovascularization Ingrowth",
    "en": "Chronic pathological tendinopathy is characterized by chaotic neovascularization accompanied by ingrowth of sensory nerve fibers, which generate recalcitrant resting pain.",
    "zh": "慢性病理性肌腱病變的組織特徵是混亂的新生微血管長入，並伴隨感覺神經纖維增生，從而產生難以消除的靜止期疼痛。",
    "tag": "#Neovascularization"
  },
  {
    "id": 70,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Spring-Mass Ankle Stiffness",
    "en": "Developing high quasi-stiffness in the ankle-Achilles spring-mass unit is vital for reducing ground contact time and recycling elastic energy during marathon racing.",
    "zh": "在踝關節與阿基里斯腱組成的彈簧質量系統中培養高度剛性，對於縮短觸地時間與高效回收彈性勢能至關重要。",
    "tag": "#AnkleStiffness"
  },
  {
    "id": 71,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Sinus Tarsi Syndrome",
    "en": "Persistent pain located in the anatomical depression on the outer side of the ankle joint following an inversion sprain indicates chronic inflammation within the sinus tarsi.",
    "zh": "腳踝內翻扭傷後外踝前下方解剖凹陷處持續深層疼痛，代表跗骨竇內部韌帶結構已陷入慢性滑膜發炎。",
    "tag": "#SinusTarsi"
  },
  {
    "id": 72,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Tibialis Anterior Tendinopathy",
    "en": "Downhill road pounding can overload the tibialis anterior tendon over the front of the ankle, producing crepitus and weakness when lifting the foot.",
    "zh": "下坡路跑的高速衝擊會使踝關節前方的脛前肌腱超載，在抬起腳背時產生摩擦音並伴隨背屈無力。",
    "tag": "#TibialisAnterior"
  },
  {
    "id": 73,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Chronic Ankle Instability (CAI)",
    "en": "Failure to retrain fibular proprioceptors following an ankle sprain develops chronic ankle instability, giving runners the distressing feeling of the joint 'giving way.'",
    "zh": "扭傷後若未及時進行腓骨本體感覺神經肌肉再訓練會演變為慢性踝關節不穩定，使跑者產生關節隨時可能失控打滑的恐懼感。",
    "tag": "#CAIInstability"
  },
  {
    "id": 74,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Isometric Tendon Analgesia",
    "en": "Performing 45-second heavy isometric heel raises induces immediate cortical inhibition and provides profound short-term pain relief for reactive Achilles tendinopathy.",
    "zh": "進行四十五秒的高負重等長提踵抗阻能引發中樞皮質神經抑制，為反應性阿基里斯腱病變提供顯著的短期止痛效益。",
    "tag": "#IsometricAnalgesia"
  },
  {
    "id": 75,
    "cat_id": "ankle",
    "cat_zh": "踝關節與肌腱",
    "injury": "Tendon De-loading and Heel Lifts",
    "en": "Temporarily inserting a 6mm to 9mm firm silicone heel wedge inside the running shoe reduces peak tensile strain across the Achilles tendon during acute flare-ups.",
    "zh": "在跑鞋內暫時墊入六至九毫米的堅固矽膠鞋跟墊，能有效卸除急性發作期阿基里斯腱所承受的峰值拉伸應變。",
    "tag": "#HeelLiftDeload"
  },
  {
    "id": 76,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Medial Tibial Stress Syndrome (MTSS)",
    "en": "Diffuse tenderness stretching along the posteromedial border of the distal tibia represents medial tibial stress syndrome, resulting from bone overload bending stress.",
    "zh": "沿著脛骨遠端後內側邊緣蔓延五公分以上的瀰漫性壓痛代表脛前痛（MTSS），其本質是脛骨骨骼彎曲應力過載所致。",
    "tag": "#MTSSShinSplints"
  },
  {
    "id": 77,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Tibial Stress Fracture",
    "en": "Sharp focal pain confined to a single pinpoint location along the tibia that hurts during gentle hopping and vibrates painfully on tuning fork tests indicates a stress fracture.",
    "zh": "局限於脛骨單一定點的劇烈針尖銳痛，在單腳跳躍或音叉震動測試時產生劇烈骨痛，直接預示著疲勞性骨折。",
    "tag": "#TibialStressFracture"
  },
  {
    "id": 78,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Chronic Exertional Compartment Syndrome (CECS)",
    "en": "When prolonged running inflates leg muscles within unyielding deep fascial sheaths, intracompartmental pressure surges beyond capillary pressure, cutting off muscle oxygen.",
    "zh": "持續跑步使小腿肌肉在缺乏彈性的緻密深筋膜內腫脹充血時，腔室內壓力會激增超越毛細血管灌流壓，切斷肌肉供氧。",
    "tag": "#CECSIschemia"
  },
  {
    "id": 79,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Soleus Strain vs Gastrocnemius Tear",
    "en": "A deep, low-lying ache in the lower third of the calf exacerbated by bent-knee walking points to a soleus strain, whereas a sudden pop high up indicates a gastrocnemius tear.",
    "zh": "小腿下三分之一處在屈膝負重行走時加劇的深層酸痛通常是比目魚肌拉傷，而高位突發爆裂聲則代表腓腸肌撕裂。",
    "tag": "#SoleusVsGastrocnemius"
  },
  {
    "id": 80,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Medial Gastrocnemius Tear ('Tennis Leg')",
    "en": "An explosive acceleration out of a water station can acutely tear the medial musculotendinous junction of the gastrocnemius, producing intense pain mimicking an Achilles snap.",
    "zh": "在補給站出站時的爆發加速可能使腓腸肌內側肌腱交界處急性撕裂（網球腿），產生類似阿基里斯腱斷裂的劇烈劇痛。",
    "tag": "#TennisLeg"
  },
  {
    "id": 81,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Anterior Tibial Cortex Stress Fracture",
    "en": "Stress fractures occurring on the anterior 'tension side' of the tibial cortex exhibit notorious non-union rates and frequently demand prolonged immobilization or surgical pinning.",
    "zh": "發生在脛骨前側「張力側」的皮質疲勞性骨折癒合率極低且容易不癒合，往往需要長時間嚴格石膏固定甚至手術釘骨加固。",
    "tag": "#TensionSideFracture"
  },
  {
    "id": 82,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Tibial Bending Moment Biomechanics",
    "en": "With every step of high-speed running, dynamic muscle contractions and ground impact bend the tibia forward, creating high compressive stresses posteriorly and tensile stresses anteriorly.",
    "zh": "在高速跑步的每一步中，動態肌肉收縮與地面衝擊會使脛骨向前微幅彎曲，在其後側產生巨大壓應力而在前側產生拉應力。",
    "tag": "#TibialBending"
  },
  {
    "id": 83,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Deep Vein Thrombosis (DVT) in Runners",
    "en": "Unilateral deep calf swelling, warmth, and erythema following a long marathon flight should never be dismissed as simple muscle soreness, as it may signal life-threatening DVT.",
    "zh": "長途飛行參加馬拉松後若出現單側小腿深層腫脹、發熱與紅斑，切勿誤當作普通肌肉酸痛，因其可能預示著致命的深層靜脈栓塞。",
    "tag": "#RunnerDVT"
  },
  {
    "id": 84,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Fasciotomy for Compartment Decompression",
    "en": "When conservative physical therapy fails to relieve chronic compartment syndrome, surgical fasciotomy cuts open the rigid fascial walls to permanently restore vascular perfusion.",
    "zh": "當保守物理治療無法緩解慢性腔室症候群時，外科筋膜切開減壓手術會切開堅硬的筋膜外壁，永久恢復肌肉的血液灌流。",
    "tag": "#SurgicalFasciotomy"
  },
  {
    "id": 85,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Shin Splints Traction Hypothesis Debunked",
    "en": "Modern histology demonstrates that shin splints is fundamentally a bone stress remodeling failure of the tibial cortex, rather than mere periosteal pulling by the tibialis posterior.",
    "zh": "現代組織病理學證實脛前痛本質上是脛骨骨皮質的骨骼應力重塑衰竭，而非單純脛後肌對骨膜的機械牽拉。",
    "tag": "#ShinSplintFact"
  },
  {
    "id": 86,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Peroneal Nerve Entrapment at Fibular Head",
    "en": "Compression of the common peroneal nerve as it curves around the neck of the fibula causes foot drop and tingling sensations across the anterior-lateral lower leg and foot dorsum.",
    "zh": "腓總神經在繞過腓骨頸部時受到壓迫，會引發垂足失能並在小腿前外側與腳背產生如螞蟻爬行的麻木刺痛。",
    "tag": "#PeronealNerveEntrapment"
  },
  {
    "id": 87,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Soleus 8x Bodyweight Force Tolerance",
    "en": "The soleus muscle must withstand up to eight times bodyweight in vertical ground reaction forces during mid-stance, highlighting its role as the ultimate endurance motor.",
    "zh": "比目魚肌在支撐中期必須承受高達八倍體重的垂直地面反作用力，凸顯出其作為終極耐力發動機的核心地位。",
    "tag": "#Soleus8xLoad"
  },
  {
    "id": 88,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Bone Stress Continuum (Reaction to Fracture)",
    "en": "Bone stress injuries progress along a continuum from asymptomatic periosteal micro-crack remodeling to painful marrow edema, cortical micro-cracking, and finally complete structural fracture.",
    "zh": "骨骼應力損傷是漸進發展的病程：從無症狀骨膜微裂痕重塑，惡化至骨髓水腫、骨皮質微骨折，最終演變為完全結構性骨折。",
    "tag": "#BoneStressContinuum"
  },
  {
    "id": 89,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Drop Landing and Shin Loading Rate",
    "en": "Runners who generate a steep initial ground impact loading rate transmit violent shock waves straight up the tibia, significantly elevating stress fracture incidence.",
    "zh": "著地時若產生陡峭的初始衝擊加載率，會將猛烈的震波直接向上传導穿透脛骨，大幅抬升疲勞性骨折的發生率。",
    "tag": "#ImpactLoadingRate"
  },
  {
    "id": 90,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Tibialis Anterior Fatigue and Slap Foot",
    "en": "Fatigue of the tibialis anterior muscle impairs eccentric dorsiflexion control during heel strike, causing the forefoot to slap loudly and uncontrolled onto the pavement.",
    "zh": "脛前肌過度疲勞會損害腳跟著地時的離心背屈控制力，導致前足在著地後發出響亮失控的拍地啪噠聲（拍地步態）。",
    "tag": "#SlapFootGait"
  },
  {
    "id": 91,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Calf Cramp and Neuromuscular Spindle Overload",
    "en": "True exercise-associated muscle cramps originate primarily from altered neuromuscular control, where fatigued muscle spindles become hyperactive while Golgi tendon organs are inhibited.",
    "zh": "運動型小腿抽筋主要源於神經肌肉控制失調：疲勞使肌梭反射極度過敏，同時高爾基腱器官的放鬆抑制機制被異常關閉。",
    "tag": "#CrampNeuromuscular"
  },
  {
    "id": 92,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Post-Run Calf Compartment Tightness",
    "en": "Resting calf tightness that persists longer than an hour after running accompanied by pale, cold toes requires immediate emergency medical evaluation for compartment ischemia.",
    "zh": "跑後小腿深層緊繃若持續超過一小時且腳趾冰冷蒼白，必須立刻前往急診評估是否存在急性腔室缺血。",
    "tag": "#CompartmentWarning"
  },
  {
    "id": 93,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Fibular Stress Fracture",
    "en": "A stress fracture located in the distal third of the slender fibula generates lateral lower leg pain that responds favorably to active rest within four to six weeks.",
    "zh": "位於細長腓骨下三分之一處的疲勞性骨折會引發小腿外側下段酸痛，在四至六週的積極休跑調整後通常癒合良好。",
    "tag": "#FibularStress"
  },
  {
    "id": 94,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Lower Leg Bone Mineral Density (BMD)",
    "en": "Low energy availability combined with high training volumes suppresses estrogen and testosterone, leaching bone mineral density and quadrupling tibial stress fracture risks.",
    "zh": "相對能量不足（RED-S）結合高跑量會抑制雌激素與睪固酮分泌，侵蝕骨骼礦物質密度並使脛骨骨折風險翻兩番。",
    "tag": "#BoneDensityBMD"
  },
  {
    "id": 95,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Eccentric Soleus Calf Raises",
    "en": "Bent-knee eccentric calf raises performed on an elevated ledge selectively isolate the soleus muscle, restoring tissue capacity against recurring deep calf strains.",
    "zh": "在墊高踏階上進行屈膝離心提踵訓練能高度孤立比目魚肌，重建組織承載力以防範復發性深層小腿拉傷。",
    "tag": "#BentKneeCalfRaise"
  },
  {
    "id": 96,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Shin Compression Sleeves Efficacy",
    "en": "Medical-grade graduated compression sleeves improve calf venous return and reduce soft tissue oscillating vibrations, decreasing perceived post-run soreness.",
    "zh": "醫療級漸進式壓縮小腿套能促進小腿靜脈回流並減少肌肉軟組織的震盪晃動，顯著減輕跑後的自覺酸痛感。",
    "tag": "#CompressionSleeves"
  },
  {
    "id": 97,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Gastrocnemius Equinus Deformity",
    "en": "Isolated tightness of the gastrocnemius limits ankle dorsiflexion when the knee is fully straight, overloading both the plantar fascia and anterior tibial bone cortex.",
    "zh": "腓腸肌攣縮會在膝蓋伸直時顯著限制踝關節背屈角度，將超額負荷同時轉嫁至足底筋膜與脛骨前側皮質。",
    "tag": "#GastrocnemiusEquinus"
  },
  {
    "id": 98,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Micro-Vascular Calf Perfusion Pressure",
    "en": "Elevated intramuscular tissue pressure during long runs reduces the arteriovenous gradient, decreasing oxygen delivery and accelerating premature muscular failure.",
    "zh": "長跑中小腿肌肉內組織壓力的升高會縮小動靜脈壓力梯度，大幅削減氧氣輸送並加速肌肉過早力竭萎縮。",
    "tag": "#CalfPerfusion"
  },
  {
    "id": 99,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Shin Palpation Diagnostic Sign",
    "en": "Gentle fingertip percussion directly over a stress fracture elicits an exquisite, sharp focal pain that causes the runner to wince immediately.",
    "zh": "用手指指腹在疲勞性骨折處直接輕敲叩診，會引發極為銳利刺骨的定點劇痛，令跑者瞬間倒抽一口氣。",
    "tag": "#FingertipPercussion"
  },
  {
    "id": 100,
    "cat_id": "shin",
    "cat_zh": "小腿與脛骨",
    "injury": "Shock Wave Therapy for Shin Splints",
    "en": "Extracorporeal radial shock wave therapy stimulates local neovascularization and triggers osteoblast proliferation, accelerating recovery from chronic recalcitrant MTSS.",
    "zh": "體外發散式震波治療能刺激局部微血管新生並促使成骨細胞增殖，加速頑固性慢性脛前痛的組織癒合。",
    "tag": "#ShockWaveMTSS"
  },
  {
    "id": 101,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Proximal Hamstring Tendinopathy (PHT)",
    "en": "Deep aching pain centered directly on the ischial tuberosity (the sit bone) that worsens when sitting on hard chairs or running uphill indicates proximal hamstring tendinopathy.",
    "zh": "正對坐骨結節處的深層酸痛，在久坐硬椅或上坡奔跑時顯著加劇，代表膕旁肌近端肌腱病變。",
    "tag": "#PHTSitBone"
  },
  {
    "id": 102,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Acute Hamstring Tear at Terminal Swing",
    "en": "The biceps femoris reaches peak elongation and active tension during the terminal swing phase of sprinting, which is when the vast majority of acute hamstring tears occur.",
    "zh": "股二頭肌在高速衝刺的擺盪末端達到最大伸展長度與主動張力極限，這正是絕大多數急性膕繩肌撕裂爆發的瞬間。",
    "tag": "#TerminalSwingTear"
  },
  {
    "id": 103,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Nordic Hamstring Curl Eccentric Strength",
    "en": "Integrating Nordic hamstring curls into your weekly strength routine increases hamstring fascicle length and shifts the optimal muscle operating length to wider joint angles.",
    "zh": "將北歐膕繩肌離心彎舉納入每週重訓計畫，能顯著增加肌束長度並將肌肉最佳做功長度外移至更大的關節角度。",
    "tag": "#NordicCurlStrength"
  },
  {
    "id": 104,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Rectus Femoris Strain",
    "en": "The rectus femoris is the only quadriceps muscle crossing both the hip and knee joints, making it uniquely vulnerable to tearing during explosive forward hip flexion and toe-off.",
    "zh": "股直肌是股四頭肌群中唯一同時跨越髖關節與膝關節的雙關節肌，在爆發性前屈髖與蹬地瞬間特別容易發生撕裂傷。",
    "tag": "#RectusFemoris"
  },
  {
    "id": 105,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Adductor Longus Strain (Groin Pull)",
    "en": "A sharp, stabbing pain near the pubic bone during directional changes or when attempting to kick forward indicates an acute strain of the adductor longus muscle.",
    "zh": "在跑動變向或向前邁步時恥骨周圍出現如刀割般的劇痛，代表大腿長收肌已發生急性鼠蹊部拉傷。",
    "tag": "#AdductorStrain"
  },
  {
    "id": 106,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Ischial Tuberosity Enthesopathy",
    "en": "Compressive shear forces generated when the hamstring tendon wraps tightly around the ischial bone during high-hip-flexion strides drive chronic degenerative enthesopathy.",
    "zh": "在高抬腿大屈髖步態中，膕繩肌腱緊密纏繞坐骨時產生的壓縮剪力，是驅動慢性退化性肌腱附著點病變的元兇。",
    "tag": "#IschialEnthesopathy"
  },
  {
    "id": 107,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Femoral Shaft Stress Fracture",
    "en": "Vague, deep-seated anterior thigh pain that worsens during weight-bearing running and exhibits a positive fulcrum test signals a dangerous femoral shaft stress fracture.",
    "zh": "大腿前側深處隱約的進行性脹痛，在承重跑步時加劇且支點測試呈陽性反應，預示著危險的股骨幹疲勞性骨折。",
    "tag": "#FemoralStressFracture"
  },
  {
    "id": 108,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Iliopsoas Tendinopathy and Bursitis",
    "en": "Pain deep in the anterior groin crease that flares when actively lifting the thigh toward the chest against resistance characterizes iliopsoas tendinopathy.",
    "zh": "鼠蹊部前側皺褶深處的隱痛，在抗阻力主動抬腿靠近胸膛時劇烈爆發，是髂腰肌肌腱炎與滑囊炎的特徵。",
    "tag": "#IliopsoasTendon"
  },
  {
    "id": 109,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Downhill Running Quadriceps Breakdown",
    "en": "Continuous steep downhill running forces the quadriceps to contract eccentrically under extreme load, rupturing myofibrils and causing severe delayed-onset muscle soreness.",
    "zh": "長距離陡峭下坡迫使股四頭肌在極重負荷下進行高強度離心收縮，造成大量肌原纖維微結構斷裂與嚴重的延遲性肌肉酸痛。",
    "tag": "#DownhillQuadBreakdown"
  },
  {
    "id": 110,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Hamstring-to-Quadriceps Imbalance",
    "en": "A pronounced imbalance where quadriceps strength completely overpowers the hamstrings creates dangerous anterior tibial shear and predisposes the runner to muscle tears.",
    "zh": "當股四頭肌力量顯著壓倒後側膕繩肌時，會造成危險的脛骨前向剪切力，大幅升高跑者肌肉撕裂與關節受損機率。",
    "tag": "#HQImbalance"
  },
  {
    "id": 111,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Vastus Lateralis Overactivity",
    "en": "An overactive, hypertonic vastus lateralis muscle exerts excessive lateral tension on the patella, worsening anterior knee pain unless relieved by deep tissue mobilization.",
    "zh": "過度活躍與僵硬痙攣的股外側肌會對髕骨施加巨大的外向牽拉張力，除非透過深層筋膜釋放，否則前膝痛將持續惡化。",
    "tag": "#VastusLateralis"
  },
  {
    "id": 112,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Hamstring Isometric Bridge Loading",
    "en": "Progressive single-leg isometric hamstring bridges performed at varying knee angles stimulate tendon healing without generating harmful compressive friction at the bone.",
    "zh": "在不同屈膝角度下進行漸進式單腿等長膕繩肌橋式訓練，能在不對坐骨產生有害壓縮摩擦的前提下有效刺激肌腱修復。",
    "tag": "#HamstringBridge"
  },
  {
    "id": 113,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Athletic Pubalgia (Sports Hernia)",
    "en": "Shearing instability between the rectus abdominis insertion and the adductor longus origin on the pubic symphysis leads to chronic groin pain known as athletic pubalgia.",
    "zh": "腹直肌附著點與長收肌起點在恥骨聯合處的剪切性微失衡，會引發稱為運動型疝氣（運動型恥骨痛）的頑固性鼠蹊痛。",
    "tag": "#AthleticPubalgia"
  },
  {
    "id": 114,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Overstriding Hamstring Strain",
    "en": "Reaching forward with an extended knee during initial contact forces the hamstring to brake the forward momentum at maximum stretch, massively elevating strain risk.",
    "zh": "著地瞬間若膝蓋過度伸直向前盲目跨步，會迫使膕繩肌在極限拉伸位置煞停向前的身體動量，使肌肉拉傷風險急劇飆升。",
    "tag": "#OverstrideHamstring"
  },
  {
    "id": 115,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Sartorius Muscle Tendinopathy",
    "en": "The long, strap-like sartorius muscle can become inflamed along its proximal origin near the anterior superior iliac spine, producing superficial anterior hip pinching.",
    "zh": "長帶狀的縫匠肌若在其靠近髂前上棘（ASIS）的近端起點處發炎，會在髖關節前側淺層產生銳利的夾擠刺痛感。",
    "tag": "#SartoriusTendon"
  },
  {
    "id": 116,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Gracilis Tendon Strain",
    "en": "The gracilis muscle assists in medial knee stabilization; overpronation and sudden trail slips can induce an acute strain along its slender medial thigh belly.",
    "zh": "股薄肌輔助維持內側膝關節穩定；在越野滑倒或過度內旋時，其細長的大腿內側肌腹容易發生急性牽拉挫傷。",
    "tag": "#GracilisStrain"
  },
  {
    "id": 117,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Delayed-Onset Muscle Soreness (DOMS) vs Tear",
    "en": "Bilateral diffuse stiffness peaking 48 hours after a marathon represents harmless DOMS, whereas sudden sharp focal pain causing a limp signals an acute muscle tear.",
    "zh": "全馬賽後四十八小時達到頂峰的雙側對稱瀰漫性僵硬是無害的 DOMS，而突發的單側定點銳痛伴隨跛行則預示著肌肉撕裂。",
    "tag": "#DOMSvsTear"
  },
  {
    "id": 118,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Hamstring Fascicle Length Adaptation",
    "en": "Eccentric strength training increases the number of sarcomeres in series, lengthening muscle fascicles and reducing susceptibility to active strain injury.",
    "zh": "離心肌力訓練能串聯增加肌節數量並有效拉長肌纖維束長度，大幅降低肌肉在主動拉伸狀態下受傷的脆弱性。",
    "tag": "#FascicleLength"
  },
  {
    "id": 119,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Sciatic Nerve Gliding over Hamstring",
    "en": "Scar tissue from previous proximal hamstring tears can entrap and adhere the adjacent sciatic nerve, generating radiating neural tightness down into the calf.",
    "zh": "舊有膕繩肌近端撕裂所殘留的疤痕組織可能黏連並夾擠相鄰的坐骨神經，產生向下放射至小腿的神經性緊繃刺痛。",
    "tag": "#SciaticNerveGliding"
  },
  {
    "id": 120,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Quadriceps Tendon Calcification",
    "en": "Chronic unresolved tendinitis can induce dystrophic calcification deposits within the quadriceps tendon insertion, visible on X-ray and requiring shock wave therapy.",
    "zh": "長期未妥善處理的慢性肌腱炎可能在股四頭肌腱附著處引發營養不良性鈣化沉積，需透過 X 光確認並施以震波治療。",
    "tag": "#TendonCalcification"
  },
  {
    "id": 121,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Biceps Femoris Short Head Tendonitis",
    "en": "The mono-articular short head of the biceps femoris can be selectively overloaded during aggressive trail ascents where sustained deep knee flexion is demanded.",
    "zh": "在需要持續深屈膝的大坡度越野攀登中，單關節的股二頭肌短頭容易被選擇性過載並引發局部發炎疼痛。",
    "tag": "#BicepsShortHead"
  },
  {
    "id": 122,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Semimembranosus Insertional Strain",
    "en": "The complex multi-armed distal insertion of the semimembranosus tendon on the posteromedial tibial condyle can mimic a posterior horn medial meniscus tear.",
    "zh": "半膜肌肌腱在脛骨後內側髁複雜的多分支遠端附著點拉傷，其臨床症狀極度類似內側半月板後角的撕裂痛感。",
    "tag": "#Semimembranosus"
  },
  {
    "id": 123,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Tensor Fasciae Latae (TFL) Hypertonicity",
    "en": "When gluteus medius firing is delayed, the tensor fasciae latae becomes hyperactive to stabilize the pelvis, driving secondary IT band tension down the thigh.",
    "zh": "當臀中肌神經徵召延遲時，闊筋膜張肌（TFL）會被迫過度活躍以代償穩定骨盆，進而將極高的張力向下傳導至整個髂脛束。",
    "tag": "#TFLHypertonicity"
  },
  {
    "id": 124,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Femoral Neck Stress Fracture (Tension Side)",
    "en": "A stress fracture along the superior tension side of the femoral neck is an orthopedic emergency that risks catastrophic avascular necrosis of the femoral head if not pinned.",
    "zh": "發生在股骨頸上緣「張力側」的疲勞性骨折是骨科急症，若未立即進行手術鋼釘固定，將面臨股骨頭缺血性壞死的災難性風險。",
    "tag": "#FemoralNeckStress"
  },
  {
    "id": 125,
    "cat_id": "thigh",
    "cat_zh": "大腿與膕繩肌",
    "injury": "Hamstring Tendon Collagen Realignment",
    "en": "Heavy progressive resistance training creates mechanical strain that stimulates fibroblasts to synthesize tenascin-C and realign disordered collagen fibrils.",
    "zh": "高負重的漸進式阻力訓練能創造必要的機械應變，刺激纖維母細胞合成腱生蛋白並引導紊亂的膠原原纖維重新規則排列。",
    "tag": "#CollagenRealignment"
  },
  {
    "id": 126,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Greater Trochanteric Pain Syndrome (GTPS)",
    "en": "Pain centered over the lateral hip prominence that prevents lying on that side at night represents greater trochanteric pain syndrome, involving gluteal tendinopathy and bursitis.",
    "zh": "局限於髖關節外側大轉子隆起處的劇痛，且夜間無法側臥壓迫該側，代表大轉子疼痛症候群（涵蓋臀肌肌腱病變與滑囊炎）。",
    "tag": "#GTPSHipPain"
  },
  {
    "id": 127,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Trendelenburg Gait and Gluteus Medius Weakness",
    "en": "Weakness of the stance-leg gluteus medius causes the contralateral pelvis to drop downward during running, unleashing a destructive chain of valgus collapse down the entire leg.",
    "zh": "支撐側臀中肌無力會導致對側骨盆在跑步騰空時向下嚴重下墜（垂臀步態），在整條下肢鏈引發破壞性的連鎖動態外翻崩塌。",
    "tag": "#TrendelenburgGait"
  },
  {
    "id": 128,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Piriformis Syndrome and Sciatica",
    "en": "A hypertonic piriformis muscle compresses the sciatic nerve as it exits the greater sciatic foramen, sending searing electrical pain and tingling down into the posterior thigh.",
    "zh": "痙攣肥大的梨狀肌在坐骨神經穿出坐骨大孔時對其產生壓迫，向大腿後側一路放射出灼熱觸電般的劇烈麻痛（假性坐骨神經痛）。",
    "tag": "#PiriformisSciatica"
  },
  {
    "id": 129,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Femoroacetabular Impingement (FAI)",
    "en": "Abnormal bony morphology of the femoral head (Cam) or acetabulum (Pincer) causes premature contact during deep hip flexion, predisposing distance runners to labral tears.",
    "zh": "股骨頭（凸輪型）或髖臼（鉗型）的解剖骨性結構異常會在深蹲或大幅屈髖時產生過早撞擊，使長跑跑者極易發生髖臼關節唇撕裂。",
    "tag": "#FAIImpingement"
  },
  {
    "id": 130,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Acetabular Labral Tear",
    "en": "A torn acetabular labrum manifests as deep anterior groin catching, clicking, and a painful feeling of hip instability during repetitive stride cycles.",
    "zh": "髖臼關節唇撕裂表現為大腿鼠蹊部深層的卡鎖、彈響雜音，以及在重複跑步跨步循環中感到髖關節鬆動不穩的深層刺痛。",
    "tag": "#LabralTear"
  },
  {
    "id": 131,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Osteitis Pubis",
    "en": "Repetitive rotational and vertical shearing across the pubic symphysis provokes osteitis pubis, producing agonizing groin pain during single-leg bounding or uphill running.",
    "zh": "恥骨聯合處承受重複的旋轉與垂直剪切力會誘發恥骨炎，在單腿跳躍或上坡跑步時產生令人難以忍受的腹股溝劇痛。",
    "tag": "#OsteitisPubis"
  },
  {
    "id": 132,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Snapping Hip Syndrome (Coxa Saltans)",
    "en": "An audible or palpable snap as the iliotibial band flips over the greater trochanter or the iliopsoas tendon glides over the femoral head denotes snapping hip syndrome.",
    "zh": "髂脛束滑過大轉子或髂腰肌腱滑過股骨頭時產生的清晰彈響或跳動感，代表彈響髖症候群。",
    "tag": "#SnappingHip"
  },
  {
    "id": 133,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Gluteus Minimus Tendinitis",
    "en": "Micro-tears in the anterior insertion of the gluteus minimus tendon mimic true lumbar radiculopathy by referring dull aching pain into the lateral thigh and buttock.",
    "zh": "臀小肌腱前側附著點的微撕裂會將沉重的鈍痛放射至大腿外側與臀部深處，其臨床表現常高度模擬腰椎神經根壓迫。",
    "tag": "#GluteMinimus"
  },
  {
    "id": 134,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Sacroiliac (SI) Joint Dysfunction",
    "en": "Asymmetric impact forces from running on banked roads can twist the sacroiliac joint, provoking unilateral lower back aching and pain when bearing weight on that side.",
    "zh": "在傾斜路面上跑步所產生的不對稱衝擊力會扭轉骶髂關節，誘發單側下背痛以及在該側單腳負重時的劇烈刺痛。",
    "tag": "#SIJointDysfunction"
  },
  {
    "id": 135,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Pelvic Anterior Tilt and Hamstring Strain",
    "en": "Excessive anterior pelvic tilt driven by tight hip flexors places the hamstring muscles in chronic passive tension, dramatically increasing their risk of tearing during speedwork.",
    "zh": "緊繃的屈髖肌群所驅動的骨盆前傾會使後側膕繩肌長期處於被動拉長緊繃狀態，大幅增加其在速度訓練中撕裂的風險。",
    "tag": "#PelvicAnteriorTilt"
  },
  {
    "id": 136,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Femoral Neck Stress Fracture (Compression Side)",
    "en": "A stress fracture along the inferior compression side of the femoral neck requires immediate non-weight-bearing crutches to prevent displacement into a complete fracture.",
    "zh": "沿著股骨頸下緣「壓應力側」發生的疲勞性骨折必須立即使用拐杖絕對禁止承重，以防其位移演變為完全骨折。",
    "tag": "#CompressionSideNeck"
  },
  {
    "id": 137,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Hip Internal Rotation Deficit",
    "en": "Loss of passive hip internal rotation forces the lumbar spine and knee joint to rotate excessively to compensate during the terminal push-off phase of running.",
    "zh": "髖關節被動內旋活動度的喪失，會迫使腰椎與膝關節在跑步後蹬末期進行過度的代償性旋轉以維持前進力線。",
    "tag": "#HipInternalRotation"
  },
  {
    "id": 138,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Gluteus Maximus Weakness and Hip Extension",
    "en": "Inadequate gluteus maximus drive forces the hamstring and lumbar erector spinae muscles to overwork as compensatory hip extensors, leading to premature fatigue and injury.",
    "zh": "臀大肌徵召無力會迫使膕繩肌與腰部豎脊肌超負荷代償完成伸髖動作，導致肌肉過早衰竭並誘發連鎖拉傷。",
    "tag": "#GluteMaxWeakness"
  },
  {
    "id": 139,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Pelvic Drop Biomechanical Cost",
    "en": "Every single millimeter of excessive contralateral pelvic drop increases lateral knee joint stress by up to eight percent during stance phase.",
    "zh": "支撐期對側骨盆每多下墜一毫米，膝關節外側所承受的力學衝擊應變就會激增高達百分之八。",
    "tag": "#PelvicDropCost"
  },
  {
    "id": 140,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Deep External Hip Rotator Tightness",
    "en": "Chronically shortened deep hip external rotators, including the obturator and gemelli muscles, compress local neurovascular bundles and cause deep gluteal dull aches.",
    "zh": "閉孔肌與雙子肌等深層外旋肌群的長期攣縮，會夾擠周圍神經血管束並引發難以定位的深層臀部酸脹痛。",
    "tag": "#DeepRotatorTightness"
  },
  {
    "id": 141,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Iliac Crest Bone Contusion (Hip Pointer)",
    "en": "A direct fall onto the exposed iliac crest on a rocky trail can cause an excruciating subperiosteal hematoma that severely limits all trunk and hip movement.",
    "zh": "在岩石山徑跌倒直接撞擊裸露的髂骨脊會造成劇烈的骨膜下血腫（髖部撞傷），嚴重限制軀幹與髖部的一切活動。",
    "tag": "#HipPointerContusion"
  },
  {
    "id": 142,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Pectineus Muscle Strain",
    "en": "The deeply seated pectineus muscle can be strained during sudden slip-and-catch reactions on icy roads, producing sharp upper-inner thigh pain.",
    "zh": "位置深層的恥骨肌在結冰路面打滑並緊急自救平衡時容易發生急性拉傷，在腹股溝上內側產生銳利刺痛。",
    "tag": "#PectineusStrain"
  },
  {
    "id": 143,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Clamshell Glute Activation Protocol",
    "en": "Performing side-lying clamshells with a resistance band awakens gluteus medius motor unit firing patterns without allowing the tensor fasciae latae to take over.",
    "zh": "側臥配戴彈力帶進行蚌殼式訓練，能精準喚醒臀中肌的運動神經單元徵召，同時抑制闊筋膜張肌的過度代償代打。",
    "tag": "#ClamshellProtocol"
  },
  {
    "id": 144,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Iliolumbar Ligament Sprain",
    "en": "The strong iliolumbar ligament anchoring the fifth lumbar vertebra to the iliac crest can become sprained when running on uneven cross-country terrain with poor core stability.",
    "zh": "核心穩定度欠佳的跑者在崎嶇不平的越野草地上奔跑時，連接第五腰椎與髂骨脊的強大髂腰韌帶容易發生牽拉扭傷。",
    "tag": "#IliolumbarLigament"
  },
  {
    "id": 145,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Hip Abduction-to-Adduction Strength Ratio",
    "en": "A balanced isometric hip abduction-to-adduction strength ratio of approximately 1.0 is essential for shielding runners against chronic groin and lateral knee pathologies.",
    "zh": "維持約一比一的均衡髖外展與內收等長肌力比值，對於保護跑者免於慢性鼠蹊痛與外側膝關節病變至關重要。",
    "tag": "#AbductionAdductionRatio"
  },
  {
    "id": 146,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Ischiofemoral Impingement",
    "en": "Narrowing of the anatomical space between the lesser trochanter and the ischial tuberosity compresses the quadratus femoris muscle, provoking posterior hip gluteal pain.",
    "zh": "股骨小轉子與坐骨結節之間的解剖間隙狹窄會夾擠股方肌，引發後髖部與坐骨深處的夾擠性臀痛。",
    "tag": "#IschiofemoralImpingement"
  },
  {
    "id": 147,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Pelvic Ring Asymmetry and Leg Length Discrepancy",
    "en": "Functional leg length discrepancy resulting from sacroiliac torsion causes uneven ground impact absorption, subjecting the longer leg to higher stress fracture risks.",
    "zh": "源於骶髂關節旋轉扭曲的功能性長短腿會造成不對稱的地面衝擊吸收，使長腿側承受翻倍的疲勞性骨折風險。",
    "tag": "#LegLengthDiscrepancy"
  },
  {
    "id": 148,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Lateral Band Walk (Monster Walk) Benefit",
    "en": "Monster walks performed with resistance bands positioned around the forefeet elicit significantly higher gluteal EMG activity than bands placed around the knees.",
    "zh": "將阻力帶套在雙前足進行怪獸側向行走，相比將彈力帶套在膝蓋上，能激發顯著更高的臀中肌與外展肌肌電圖活化活性。",
    "tag": "#MonsterWalkBenefit"
  },
  {
    "id": 149,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Hip Joint Avascular Necrosis Warning",
    "en": "Unexplained, persistent deep groin pain that refuses to improve with conservative rest must be evaluated with MRI to rule out early-stage avascular necrosis of the femoral head.",
    "zh": "經過保守休跑後仍持續不退的不明深層鼠蹊痛，必須安排核磁共振（MRI）檢查以徹底排除早期股骨頭缺血性壞死。",
    "tag": "#AvascularNecrosisWarning"
  },
  {
    "id": 150,
    "cat_id": "hip",
    "cat_zh": "髖部與骨盆",
    "injury": "Pelvic Floor Dysfunction in Distance Runners",
    "en": "High repetitive intra-abdominal pressure pulses during marathon running can fatigue pelvic floor muscles, contributing to core instability and sacroiliac joint strain.",
    "zh": "馬拉松奔跑過程中腹內壓的持續高頻脈衝衝擊可能使骨盆底肌群過度疲勞，進而導致核心失穩與骶髂關節勞損。",
    "tag": "#PelvicFloorRunners"
  },
  {
    "id": 151,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Runner's Lower Back Pain (Erector Spinae Fatigue)",
    "en": "Fatigue of the deep core stabilizers shifts excessive extension loads onto the lumbar erector spinae, causing painful muscle spasms during the final miles of a marathon.",
    "zh": "深層核心穩定肌群的疲勞會將超額伸展負荷轉嫁至腰部豎脊肌，在馬拉松最後幾英里引發痛苦的下背肌肉痙攣。",
    "tag": "#LowerBackPain"
  },
  {
    "id": 152,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Lumbar Disc Herniation from Repetitive Impact",
    "en": "Repetitive axial ground reaction forces transmitted through a poorly aligned pelvis can exacerbate disc bulging, pinching nerve roots and sending radicular pain down the leg.",
    "zh": "穿透力線不良骨盆的重複性軸向衝擊力會加劇腰椎間盤突出，夾擠神經根並向下肢放射劇烈神經根性痛。",
    "tag": "#DiscHerniation"
  },
  {
    "id": 153,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Spondylolysis (Lumbar Pars Stress Fracture)",
    "en": "Hyperextension combined with rotational impact forces in endurance running can stress the pars interarticularis of the lumbar spine, triggering spondylolysis.",
    "zh": "耐力跑步中的過度伸腰結合旋轉衝擊力，會使腰椎椎弓峽部承受過度剪切張力，誘發椎弓骨折（腰椎滑脫前兆）。",
    "tag": "#Spondylolysis"
  },
  {
    "id": 154,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Core Bracing and Intra-Abdominal Pressure (IAP)",
    "en": "Actively establishing intra-abdominal pressure via diaphragmatic bracing creates a 360-degree pneumatic cylinder that unloads compressive forces from the lumbar vertebrae.",
    "zh": "透過橫膈膜支撐主動建立腹內壓，能形成三百六十度的天然氣動支撐柱，大幅卸除腰椎椎骨所承受的垂直壓縮力。",
    "tag": "#CoreBracingIAP"
  },
  {
    "id": 155,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Thoracic Spine Mobility Restriction",
    "en": "Stiffness in the thoracic spine restricts natural rotational arm swing, forcing the lumbar vertebrae to rotate pathologically and causing rotational lower back shear.",
    "zh": "胸椎活動度僵硬會限制自然的旋轉擺臂動作，迫使腰椎產生病理性的代償旋轉，引發下背旋轉剪切傷害。",
    "tag": "#ThoracicMobility"
  },
  {
    "id": 156,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Forward Head Posture Late-Race Collapse",
    "en": "Late-race fatigue often allows the head to drift forward, dramatically multiplying cervical spine loads and triggering painful upper-back trapezius spasms.",
    "zh": "賽事後段的體能疲勞常使頭部不由自主向前探出，幾何級數放大頸椎承受的重力力矩並誘發上背斜方肌劇烈痙攣。",
    "tag": "#ForwardHeadPosture"
  },
  {
    "id": 157,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Quadratus Lumborum (QL) Muscle Spasm",
    "en": "When the gluteus medius drops the hip on one side, the ipsilateral quadratus lumborum must hike the pelvis aggressively, leading to severe lateral flank spasms.",
    "zh": "當單側臀中肌無力使骨盆下墜時，同側的腰方肌（QL）必須被迫強烈提拔骨盆以作代償，引發嚴重的腰側痙攣痛。",
    "tag": "#QLSpasm"
  },
  {
    "id": 158,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Kyphotic Chest Collapse and Breathing Deficit",
    "en": "Slumping the shoulders forward collapses the rib cage, compressing the diaphragm and reducing vital lung capacity during maximum aerobic endurance efforts.",
    "zh": "含胸駝背的跑姿會壓縮胸廓並擠壓橫膈膜活動空間，在最大有氧耐力輸出時嚴重削弱肺活量與通氣效率。",
    "tag": "#KyphoticCollapse"
  },
  {
    "id": 159,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Arm Swing Asymmetry and Spinal Torsion",
    "en": "Carrying a phone or water bottle in only one hand generates an asymmetrical arm swing that produces unequal rotational torque across the lumbar spine.",
    "zh": "單手持手機或水壺跑步會產生左右不對稱的擺臂力矩，對腰椎施加不均勻的旋轉扭力與疲勞負擔。",
    "tag": "#ArmSwingAsymmetry"
  },
  {
    "id": 160,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Lumbar Facet Joint Syndrome",
    "en": "Excessive anterior pelvic tilt forces the lumbar spine into hyper-lordosis, wedging the posterior facet joints together and causing sharp localized back pain upon leaning back.",
    "zh": "過度骨盆前傾會迫使腰椎處於極端過曲前凸狀態，使後側關節突關節相互卡死擠壓，在後仰時產生尖銳的局限性背痛。",
    "tag": "#FacetJointSyndrome"
  },
  {
    "id": 161,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Transverse Abdominis (TVA) Neuromuscular Timing",
    "en": "Delayed pre-activation of the transverse abdominis fails to stabilize the pelvis prior to heel strike, leaking energy and predisposing the runner to groin strains.",
    "zh": "腹橫肌（TVA）若未能在腳跟著地前預先啟動收縮，將無法鎖定骨盆剛性，導致能量洩漏並大幅增加鼠蹊部拉傷風險。",
    "tag": "#TVATiming"
  },
  {
    "id": 162,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Sacral Stress Fracture",
    "en": "Severe aching across the buttock and sacral region that worsens progressively during running and makes standing on one leg agonizing suggests a sacral stress fracture.",
    "zh": "臀部與骶骨區域在跑步過程中持續惡化的深層劇痛，且單腿站立時痛徹心扉，強烈提示可能存在骶骨疲勞性骨折。",
    "tag": "#SacralStressFracture"
  },
  {
    "id": 163,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Multifidus Muscle Atrophy in Chronic Back Pain",
    "en": "Inhibition and fatty infiltration of the deep lumbar multifidus stabilizers compromises segmental spinal stiffness, transforming acute back soreness into chronic instability.",
    "zh": "深層腰椎多裂肌的神經抑制與脂肪浸潤會損害節段間的脊椎穩定剛性，將急性背部酸痛演變為頑固性慢性失穩。",
    "tag": "#MultifidusAtrophy"
  },
  {
    "id": 164,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Cervical Radiculopathy in Runners",
    "en": "Tense, elevated shoulders combined with heavy vertical bounding can compress cervical nerve roots, sending shooting tingling sensations down into the fingers.",
    "zh": "緊繃聳肩結合劇烈的垂直彈跳震盪會夾擠頸椎神經根，向手臂與指尖放射出觸電般的發麻刺痛感。",
    "tag": "#CervicalRadiculopathy"
  },
  {
    "id": 165,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Rib Stress Fracture from Heavy Breathing",
    "en": "Violent hyperventilation over ultramarathons combined with repetitive upper-body rotational twisting can occasionally provoke a fatigue stress fracture of the ribs.",
    "zh": "超馬過程中劇烈的高頻深呼吸通氣結合上身重複的旋轉扭轉，偶爾會誘發肋骨的疲勞性骨折。",
    "tag": "#RibStressFracture"
  },
  {
    "id": 166,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Coccyx Pain (Coccydynia) from Hard Falls",
    "en": "Slipping backward onto hard rocks during technical trail descents can bruise or fracture the tailbone, causing agonizing pain when sitting or running downhill.",
    "zh": "在崎嶇越野下坡時向後滑倒重重跌坐於岩石上會挫傷或折斷尾椎骨，造成久坐或下坡跑動時難以忍受的尾骨劇痛。",
    "tag": "#CoccyxPain"
  },
  {
    "id": 167,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Core Stiffness for Elastic Energy Transfer",
    "en": "An ultra-rigid core acts as a stiff transmission chassis, preventing rotational torsional leakage and channeling 100 percent of leg drive into forward velocity.",
    "zh": "極為剛性的核心宛如穩固的賽車底盤，能阻斷旋轉扭矩的能量洩漏，將下肢推蹬力量百分之百轉化為向前的推進速度。",
    "tag": "#CoreStiffness"
  },
  {
    "id": 168,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Lumbar Extensor Endurance Test (Biering-Sorensen)",
    "en": "An inability to maintain a horizontal torso hold for at least two minutes on the Biering-Sorensen test indicates insufficient spinal extensor endurance for marathons.",
    "zh": "若無法在索倫森測試（Biering-Sorensen）中維持水平軀幹懸空達兩分鐘，代表脊椎伸肌耐力不足以支撐全馬後段疲勞衝擊。",
    "tag": "#SorensenTest"
  },
  {
    "id": 169,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Pelvic Rotational Oscillation Energy Leak",
    "en": "Uncontrolled transverse pelvic oscillation greater than 8 degrees squanders metabolic energy and places excessive shear stress across the L5-S1 lumbosacral junction.",
    "zh": "橫向骨盆旋轉擺幅若失控超過八度，不僅會大量浪費代謝能量，還會對第五腰椎與第一骶椎接合處施加過度剪切張力。",
    "tag": "#PelvicOscillation"
  },
  {
    "id": 170,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Spinal Decompression Hang Protocol",
    "en": "Performing two minutes of passive bar hanging post-run decompresses intervertebral discs, rehydrating cartilaginous endplates after pounding road miles.",
    "zh": "跑後進行兩分鐘的單槓被動懸吊能有效對腰椎進行軸向減壓，為長途路跑衝擊後的椎間盤與軟骨終板補充水分。",
    "tag": "#SpinalDecompression"
  },
  {
    "id": 171,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Diaphragm Spasm (Side Stitch / ETAP)",
    "en": "Exercise-related transient abdominal pain (a 'side stitch') stems from peritoneal ligament strain or diaphragm ischemia provoked by shallow, irregular breathing patterns.",
    "zh": "運動型短暫腹痛（俗稱側腹痛／叉氣）源於淺而紊亂的呼吸模式所誘發的腹膜韌帶牽拉或橫膈膜局部缺血。",
    "tag": "#SideStitchETAP"
  },
  {
    "id": 172,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Oblique Muscle Strain from Trail Scrambling",
    "en": "Sudden violent torso twisting to recover balance on loose gravel trail terrain can acutely strain the internal and external abdominal oblique muscles.",
    "zh": "在鬆動碎石坡面上為急救平衡而突然猛烈扭轉軀幹，會造成腹內斜肌與腹外斜肌的急性肌肉拉傷。",
    "tag": "#ObliqueStrain"
  },
  {
    "id": 173,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Scoliosis-Induced Asymmetric Running Mechanics",
    "en": "Structural scoliosis creates an asymmetrical pelvis and unequal limb loading, predisposing one side of the body to recurrent stress fractures and tendon injuries.",
    "zh": "結構性脊椎側彎會導致骨盆傾斜與兩腿不對稱承重，使身體特定單側反覆暴露於疲勞性骨折與肌腱炎的威脅中。",
    "tag": "#ScoliosisMechanics"
  },
  {
    "id": 174,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Abdominal Wall Fatigue and Herniation Risk",
    "en": "Chronic intra-abdominal pressure pulses coupled with weak transverse abdominal fascia can lead to direct or indirect inguinal hernia development in masters runners.",
    "zh": "慢性高強度腹內壓脈衝結合薄弱的腹壁筋膜，可能會在高齡長跑跑者中誘發直疝或斜疝等腹股溝疝氣。",
    "tag": "#HerniaRisk"
  },
  {
    "id": 175,
    "cat_id": "spine",
    "cat_zh": "脊椎與核心",
    "injury": "Active Neutral Spine Alignment",
    "en": "Maintaining an active neutral spine with a slight forward lean from the ankles prevents lumbar hyper-lordosis while maximizing gravity-assisted forward momentum.",
    "zh": "維持以腳踝為支點微幅前傾的主動中立脊椎姿態，既能杜絕腰椎過度前凸折損，又能最大化重力輔助的向前滑行推進效率。",
    "tag": "#NeutralSpine"
  },
  {
    "id": 176,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Exertional Rhabdomyolysis",
    "en": "Severe muscle breakdown during ultramarathons releases massive amounts of intracellular myoglobin into the circulation, producing dark tea-colored urine and kidney failure.",
    "zh": "超馬過程中嚴重的橫紋肌破壞會將大量細胞內肌紅蛋白釋放至血液中，產生可樂色濃茶尿並引發急性腎衰竭。",
    "tag": "#Rhabdomyolysis"
  },
  {
    "id": 177,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Exertional Heat Stroke (EHS)",
    "en": "A core body temperature spiking above 40.5 degrees Celsius accompanied by confusion or collapse constitutes exertional heat stroke, an immediate medical emergency.",
    "zh": "核心體溫飆升突破攝氏四十點五度並伴隨中樞神經神智混亂或昏厥，即構成勞力型中暑，為致死率極高的醫療急症。",
    "tag": "#HeatStroke"
  },
  {
    "id": 178,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Cold Water Immersion for Heat Stroke",
    "en": "Immediate whole-body cold water immersion with vigorous water agitation is the non-negotiable gold standard treatment that drops core temperature and saves lives in heat stroke.",
    "zh": "立即進行全身冰水浸泡並用力攪動水流以促進對流，是迅速降低核心體溫並拯救中暑跑者生命的黃金標準治療準則。",
    "tag": "#ColdWaterImmersion"
  },
  {
    "id": 179,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Exercise-Associated Hyponatremia (EAH)",
    "en": "Consuming excess plain water without adequate sodium during hot endurance events dangerously dilutes serum sodium, triggering exercise-associated hyponatremia and cerebral edema.",
    "zh": "在炎熱耐力賽中盲目過量飲用純水而未補充足量電解質鈉，會危險地稀釋血清鈉濃度，誘發運動型低鈉血症與致命腦水腫。",
    "tag": "#HyponatremiaEAH"
  },
  {
    "id": 180,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Heat Exhaustion vs Heat Stroke",
    "en": "Heat exhaustion presents with heavy sweating, nausea, and dizziness with preserved mental clarity, whereas heat stroke is defined by central nervous system dysfunction.",
    "zh": "熱衰竭表現為大汗淋漓、噁心反胃與眩暈但意識尚屬清醒，而熱中暑的核心診斷標準則是中樞神經系統功能出現錯亂障礙。",
    "tag": "#HeatExhaustion"
  },
  {
    "id": 181,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Hypothermia in Wet, Cold Races",
    "en": "Combining freezing ambient temperatures with wet clothing and gusting winds rapidly exhausts metabolic heat production, driving core body temperature below 35 degrees Celsius.",
    "zh": "低溫嚴寒結合濕透的跑服與強勁風寒效應，會迅速耗竭身體代謝產熱能力，將核心體溫打落至攝氏三十五度以下的失溫危境。",
    "tag": "#Hypothermia"
  },
  {
    "id": 182,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Paradoxical Undressing in Severe Hypothermia",
    "en": "As brain function breaks down in terminal hypothermia, victims experience a false sensation of burning heat and begin paradoxical undressing just before losing consciousness.",
    "zh": "重度失溫導致大腦體溫調節中樞崩潰時，患者會產生極度灼熱的幻覺並開始反常脫衣，隨後迅速陷入昏迷。",
    "tag": "#ParadoxicalUndressing"
  },
  {
    "id": 183,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Frostbite and Peripheral Necrosis",
    "en": "Prolonged exposure of wet fingers, toes, and earlobes to sub-zero temperatures freezes extracellular water, forming ice crystals that cause permanent ischemic tissue necrosis.",
    "zh": "潮濕的手指、腳趾或耳垂在零下氣溫中長期暴露會使細胞外液凍結形成冰晶，造成永久性的缺血性組織壞死。",
    "tag": "#FrostbiteNecrosis"
  },
  {
    "id": 184,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Cold-Induced Bronchoconstriction (CIB)",
    "en": "Inhaling high volumes of dry, sub-freezing air during winter intervals hyper-osmolarly dehydrates the airway mucosa, triggering sudden acute bronchospasm and wheezing.",
    "zh": "在嚴冬間歇跑中大量吸入乾冷空氣會使氣道黏膜高滲透壓脫水，引發突發性急性支氣管痙攣與哮鳴氣喘。",
    "tag": "#ColdBronchoconstriction"
  },
  {
    "id": 185,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Cold Gastric Distress and GI Cramps",
    "en": "Drinking icy fluids or inhaling freezing air diverts splanchnic blood flow away from the gut, triggering painful stomach cramps, severe vomiting, and gastric paralysis.",
    "zh": "飲用冰水或吸入嚴寒空氣會導致內臟微血管劇烈收縮缺血，觸發痛苦的胃痙攣、劇烈嘔吐與胃部停滯癱瘓。",
    "tag": "#ColdGIDistress"
  },
  {
    "id": 186,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Exercise-Induced Gastrointestinal Syndrome (EIGS)",
    "en": "Heavy running diverts up to 80 percent of splanchnic blood flow to working muscles and skin, inducing gut mucosal ischemia, epithelial breakdown, and bloody diarrhea.",
    "zh": "劇烈長跑會將高達百分之八十的內臟血流轉移至運動肌肉與皮膚，造成腸道黏膜缺血、上皮屏障瓦解與便血腹瀉。",
    "tag": "#EIGSGutSyndrome"
  },
  {
    "id": 187,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Runner's Anemia and Foot-Strike Hemolysis",
    "en": "Repetitive mechanical impact from feet smashing into hard pavement physically crushes red blood cells within the plantar capillaries, contributing to foot-strike hemolysis.",
    "zh": "腳底反覆猛烈重擊堅硬的水泥柏油路面，會在物理層面上直接粉碎足底毛細血管內的紅血球，造成跑者行軍性溶血性貧血。",
    "tag": "#FootStrikeHemolysis"
  },
  {
    "id": 188,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "High-Altitude Pulmonary Edema (HAPE)",
    "en": "Ascending rapidly into high mountain environments causes hypoxic pulmonary vasoconstriction, dangerously elevating pulmonary arterial pressure and leaking fluid into alveoli.",
    "zh": "快速攀登至高海拔山徑會誘發嚴重的缺氧性肺血管收縮，使肺動脈壓危險飆升並將組織液滲漏至肺泡引發高山肺水腫。",
    "tag": "#HAPEPulmonaryEdema"
  },
  {
    "id": 189,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "High-Altitude Cerebral Edema (HACE)",
    "en": "Severe hypoxia-induced blood-brain barrier disruption causes brain swelling, producing ataxic drunkenness, severe confusion, and rapid coma unless immediately descended.",
    "zh": "嚴重缺氧破壞血腦屏障會誘發高山腦水腫，產生醉酒般步態失調、嚴重意識混亂並迅速昏迷，唯一生機是立即下撤海拔。",
    "tag": "#HACECerebralEdema"
  },
  {
    "id": 190,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Blunt Ocular Trauma from Low-Hanging Trail Branches",
    "en": "Running through dense trail foliage in low-light conditions poses a severe risk of corneal abrasion or eyeball perforation from whipping low-hanging branches.",
    "zh": "在光線昏暗的山林山徑中疾馳穿梭，極易被反彈的低垂尖銳枝枒抽擊眼球，引發角膜嚴重刮傷甚至眼球破裂穿孔。",
    "tag": "#OcularTrauma"
  },
  {
    "id": 191,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Photokeratitis (Snow Blindness)",
    "en": "High UV radiation reflected off snowfields or white limestone trails without polarized eye protection sunburns the corneal epithelium, causing excruciating photokeratitis.",
    "zh": "在雪地或反光強烈的白石灰岩山徑上奔跑若未配戴抗 UV 防護鏡，強烈紫外線會曬傷角膜上皮，引發痛如刀割的雪盲性角膜炎。",
    "tag": "#SnowBlindness"
  },
  {
    "id": 192,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Hornet Attacks and Systemic Anaphylaxis",
    "en": "Trail runners disturbing an aggressive hornet nest can suffer multiple stings that trigger fatal systemic anaphylactic shock, requiring immediate intramuscular epinephrine.",
    "zh": "越野跑者若不慎驚擾具有強烈攻擊性的虎頭蜂群，遭受連續螫刺可能引發致命的全身性過敏休克，必須立刻注射腎上腺素（EpiPen）。",
    "tag": "#HornetAnaphylaxis"
  },
  {
    "id": 193,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Wilderness Hypothermia Shelter Bivy Protocol",
    "en": "When an injured trail runner is stranded in the mountains, deploying an aluminized emergency survival bivy sack stops radiant heat loss and shields from deadly wind chill.",
    "zh": "當受傷的越野跑者受困於高山時，立刻展開鋁箔緊急求生露宿袋能阻斷體表輻射熱散失，並防禦致命的刺骨風寒效應。",
    "tag": "#BivyShelterProtocol"
  },
  {
    "id": 194,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Satellite SOS Alpine Distress Activation",
    "en": "When a mountain accident occurs outside cellular coverage, activating a dedicated two-way satellite communicator broadcasts precise GPS coordinates to search and rescue teams.",
    "zh": "當山野意外發生在無手機基地台收訊死角時，啟動雙向衛星通訊求救設備能將精確的 GPS 經緯度座標直傳給搜救團隊。",
    "tag": "#SatelliteSOS"
  },
  {
    "id": 195,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Flash Flood Trail Crossing Danger",
    "en": "Attempting to wade across knee-deep, muddy mountain torrents after sudden cloudbursts risks being swept away by powerful hydraulic forces and drowning.",
    "zh": "在午後雷陣雨山洪爆發後若強行涉水渡過水深及膝的湍急泥流，極易被強大水流衝倒捲走造成溺水滅頂。",
    "tag": "#FlashFloodCrossing"
  },
  {
    "id": 196,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "PM2.5 Air Pollution and Cardiovascular Strain",
    "en": "Inhaling fine particulate matter during intense outdoor running promotes systemic vascular inflammation, induces endothelial dysfunction, and elevates acute cardiac event risks.",
    "zh": "在戶外劇烈奔跑時吸入高濃度 PM2.5 細懸浮微粒會引發全身性血管發炎反應、損害內皮功能並倍增急性心血管事件風險。",
    "tag": "#PM25Pollution"
  },
  {
    "id": 197,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Exercise-Induced Ischemic Colitis",
    "en": "Profound shunting of mesenteric blood flow during a grueling hot marathon can cause transient mucosal ischemia of the colon, producing severe cramping and bloody stools.",
    "zh": "在酷熱嚴峻的全馬賽程中腸繫膜血流的深度分流轉移，可能引發結腸暫時性缺血壞死，造成劇烈腹部絞痛與血便便血。",
    "tag": "#IschemicColitis"
  },
  {
    "id": 198,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Heat Syncope (Post-Finish Line Collapse)",
    "en": "Abruptly halting after crossing the marathon finish line causes massive pooling of blood in dilated lower-limb venous beds, inducing brain hypoperfusion and heat syncope.",
    "zh": "跑過馬拉松終點線後若突然靜止站立，會使大量血液淤積在極度擴張的下肢靜脈中，導致大腦供血不足而引發神經性中暑昏厥。",
    "tag": "#HeatSyncope"
  },
  {
    "id": 199,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Lightning Strike Hazard on Exposed Ridges",
    "en": "Trail runners caught on barren, exposed mountain ridges during sudden thunderstorms become the tallest conductor, inviting lethal direct lightning strikes.",
    "zh": "在突發雷暴中滯留於毫無植被遮蔽的高山稜線上的越野跑者會成為最突出的避雷導體，面臨致命雷擊直擊的極度威脅。",
    "tag": "#LightningHazard"
  },
  {
    "id": 200,
    "cat_id": "systemic",
    "cat_zh": "環境與代謝急症",
    "injury": "Hypoglycemic Mental Collapse ('The Bonk')",
    "en": "Complete depletion of hepatic glycogen stores during long running deprives the central nervous system of glucose, triggering severe ataxia, tunnel vision, and cognitive collapse.",
    "zh": "長跑過程中若肝醣徹底耗竭，會直接切斷中樞神經系統的葡萄糖供應，誘發嚴重的步態失調、管狀視野與認知崩潰（撞牆期）。",
    "tag": "#HypoglycemicBonk"
  },
  {
    "id": 201,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Forward Head Posture & Runner's Kyphosis",
    "en": "Excessive forward head posture and rounded shoulders compress the thoracic outlet, causing early arm numbness and reducing diaphragm respiratory excursion during marathon late stages.",
    "zh": "過度頭部前傾與圓肩駝背會壓迫胸廓出口，在馬拉松後半程引發手臂發麻並降低橫膈膜呼吸活動度。",
    "tag": "#UpperPosturalStrain"
  },
  {
    "id": 202,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Rotator Cuff Impingement & Sprint Arm Drive",
    "en": "Imbalanced shoulder internal rotation without adequate supraspinatus and infraspinatus strength predisposes sprinters to subacromial impingement during aggressive contralateral arm swings.",
    "zh": "若缺乏足夠的棘上肌與棘下肌肌力，失衡的肩內旋會使短跑選手在劇烈對側擺臂時引發肩峰下夾擠症候群。",
    "tag": "#RotatorCuff"
  },
  {
    "id": 203,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Scapular Winging & Serratus Anterior Weakness",
    "en": "Weakness in the serratus anterior muscle leads to scapular winging, destabilizing the upper torso and transferring disruptive torsional shock to the cervical spine with every foot strike.",
    "zh": "前鋸肌無力會引發肩胛翼狀突出，破壞上半身軀幹穩定性，並在每次著地時將破壞性扭轉震波傳遞至頸椎。",
    "tag": "#ScapularWinging"
  },
  {
    "id": 204,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Upper Trapezius Hypertonicity & Neck Tension",
    "en": "Chronically hiking the shoulders upward during distance fatigue triggers severe upper trapezius spasms, causing radiating occipital tension headaches that hinder pacing focus.",
    "zh": "在長跑疲憊時長期不自覺聳肩會誘發嚴重的上斜方肌痙攣，引發放射至枕骨的緊張性頭痛並破壞配速專注力。",
    "tag": "#NeckTension"
  },
  {
    "id": 205,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Biceps Tendon Subluxation & Cross-Body Swing",
    "en": "Allowing the hands to cross the torso midline creates repetitive friction along the bicipital groove, provoking anterior shoulder pain and biceps tenosynovitis.",
    "zh": "跑步時雙手越過軀幹中線會沿著結節間溝產生反覆摩擦，誘發前肩刺痛與二頭肌長頭腱鞘炎。",
    "tag": "#BicepsTendon"
  },
  {
    "id": 206,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Pectoralis Minor Tightness & Nerve Compression",
    "en": "Shortened pectoralis minor muscles pull the coracoid process anteriorly, entrapping the brachial plexus nerves and producing distal forearm tingling during continuous distance efforts.",
    "zh": "縮短緊繃的胸小肌會將喙突向前下方牽引，卡壓臂神經叢並在長時間耐力奔跑中引起前臂遠端麻木。",
    "tag": "#PecMinorTOS"
  },
  {
    "id": 207,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Rhomboid Strain & Hydration Pack Overload",
    "en": "Carrying a poorly fitted hydration vest over ultra-marathon terrain places prolonged tensile strain on the rhomboid major, leading to burning interscapular muscular exhaustion.",
    "zh": "在超馬越野地形中揹負貼合不良的補水背心會對大菱形肌造成持續拉扯，引發兩肩胛骨間灼熱性肌肉衰竭。",
    "tag": "#RhomboidStrain"
  },
  {
    "id": 208,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Thoracic Hypomobility & Pelvic Torque Leakage",
    "en": "Stiff thoracic vertebrae force the lumbar spine and pelvis to undergo excessive twisting, increasing rotational shear on the sacroiliac joint and gluteal attachments.",
    "zh": "僵硬受限的胸椎會迫使腰椎與骨盆產生代償性過度扭轉，增加薦髂關節與臀肌附著點的旋轉剪切力。",
    "tag": "#ThoracicMobility"
  },
  {
    "id": 209,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Elbow Angle Collapse & Triceps Kinetic Loss",
    "en": "Opening the elbow joint past ninety degrees during arm recovery increases the moment arm of the limb, wasting significant metabolic energy and lowering running cadence.",
    "zh": "在擺臂回彈時手臂肘關節角度若超過九十度，會增大上肢力臂半徑，浪費顯著的代謝能量並拖慢步頻節奏。",
    "tag": "#ElbowKinematics"
  },
  {
    "id": 210,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Overhead Press Strength & Scapular Elevation",
    "en": "Performing strict overhead dumbbell presses develops the lower trapezius and serratus anterior, reinforcing the scapular upward rotation necessary to sustain upright distance posture.",
    "zh": "執行標準啞鈴過頂肩推能強化下斜方肌與前鋸肌，增強肩胛骨上迴旋力道以維持挺拔的長跑身姿。",
    "tag": "#OverheadPress"
  },
  {
    "id": 211,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Bent-Over Rows & Posterior Torso Armor",
    "en": "Heavy bent-over barbell rows build dense latissimus dorsi and erector spinae armor, shielding distance runners from postural collapse during grueling 30K wall phases.",
    "zh": "大重量俯身槓鈴划船能構建厚實的背闊肌與豎脊肌護甲，保護長跑跑者在艱苦的三十公里撞牆期免於體態崩塌。",
    "tag": "#BentOverRow"
  },
  {
    "id": 212,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Pull-Up Dominance & Core Coupling",
    "en": "Weighted pull-ups recruit the latissimus dorsi in synergy with the contralateral gluteus maximus via the thoracolumbar fascia, supercharging horizontal running propulsion.",
    "zh": "負重引體向上透過胸腰筋膜促進背闊肌與對側臀大肌協同發力，強力提升水平推進衝力。",
    "tag": "#PullUpDrive"
  },
  {
    "id": 213,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Push-Up Variations & Anterior Core Bracing",
    "en": "Push-ups performed on gymnastic rings integrate serratus anterior activation with intense plank-style core bracing, protecting against lumbar hyperextension under fatigue.",
    "zh": "在體操吊環上執行俯臥撐結合了前鋸肌激活與高強度平板核心支撐，有效防止長跑疲憊時的腰椎過度前凸折壓。",
    "tag": "#RingPushUp"
  },
  {
    "id": 214,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Face Pulls & External Rotator Conditioning",
    "en": "Cable face pulls targeting the rear deltoids and external rotators effectively reverse the forward-hunched posture caused by desk jobs and marathon training fatigue.",
    "zh": "針對後三角肌與肩外旋肌群的滑輪面拉訓練，能有效逆轉久坐辦公與馬拉松訓練疲勞引發的圓肩駝背體態。",
    "tag": "#FacePulls"
  },
  {
    "id": 215,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Dips & Triceps Extension Power in Hill Sprints",
    "en": "Controlled bodyweight parallel bar dips strengthen the triceps and lower chest, enhancing the explosive backward arm punch required when surging up twenty-percent trail gradients.",
    "zh": "受控的自重雙槓臂屈伸能增強三頭肌與胸下側肌力，增強在攀爬百分之二十陡峭越野坡度時所需的爆發性後擺肘部推力。",
    "tag": "#ParallelBarDips"
  },
  {
    "id": 216,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Single-Arm Dumbbell Snatch & Kinetic Transfer",
    "en": "The single-arm dumbbell snatch trains instantaneous kinetic energy transfer from triple extension of the lower extremity up through the shoulder girdle to overhead lockout.",
    "zh": "單臂啞鈴抓舉能鍛鍊下肢三關節伸展瞬間將動能貫穿核心肩帶傳導至過頂鎖定的爆發傳導能力。",
    "tag": "#DumbbellSnatch"
  },
  {
    "id": 217,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Kettlebell Renegade Rows & Rotational Stability",
    "en": "Kettlebell renegade rows force the deep abdominal wall to resist rotational torque while the upper back pulls, establishing rock-solid stability for choppy downhill running.",
    "zh": "壺鈴叛徒划船迫使深層腹壁在背部划船發力時抵抗旋轉力矩，為崎嶇不平的快速下坡奔跑奠定磐石般的穩定基石。",
    "tag": "#RenegadeRow"
  },
  {
    "id": 218,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Farmer's Walk & Grip-Trapezius Structural Armor",
    "en": "Heavy farmer's walks build supreme grip strength, trapezius endurance, and lateral hip stability, teaching the body to resist asymmetrical ground shock without spinal collapse.",
    "zh": "沉重農夫行走能打造強大的握力、斜方肌耐力與外側臀肌穩定性，訓練身體在抵抗不對稱地面衝擊時保持脊柱不塌陷。",
    "tag": "#FarmersWalk"
  },
  {
    "id": 219,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Inverted Rows & Mid-Back Endurance for Pack Running",
    "en": "Suspension trainer inverted rows condition the posterior deltoids and rhomboids to maintain upright spinal posture while running with heavy multi-day stage race packs.",
    "zh": "懸吊阻力繩反向划船能訓練三角肌後束與菱形肌，使跑者在揹負多日極地超馬越野裝備時依然維持筆直脊椎姿態。",
    "tag": "#InvertedRow"
  },
  {
    "id": 220,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Landmine Press & Cross-Body Linear Drive",
    "en": "The angled landmine press closely replicates the contralateral punch of the running arm swing, strengthening the anterior deltoid and serratus without shoulder joint impingement.",
    "zh": "傾斜地雷管推舉高度模擬跑步擺臂的對側出拳發力，在不引發肩關節夾擠的前提下強化前三角肌與前鋸肌。",
    "tag": "#LandminePress"
  },
  {
    "id": 221,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Prone Y-T-W Raises & Scapular Depression",
    "en": "Performing prone Y-T-W raises on an incline bench isolates the lower trapezius and mid-back stabilizers, eradicating forward shoulder posture caused by marathon mileage volume.",
    "zh": "在斜背長凳上進行俯臥 Y-T-W 上抬動作能孤立強化下斜方肌與中背穩定肌群，根除長跑里程累積所帶來的肩部向前萎縮圓肩體態。",
    "tag": "#YTWRaises"
  },
  {
    "id": 222,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Medicine Ball Overhead Slams & Explosive Lats",
    "en": "Medicine ball overhead slams generate rapid latissimus dorsi and abdominal recruitment, converting upper body pull power into rhythmic propulsion for uphill marathon surges.",
    "zh": "藥球過頂砸地訓練能引發背闊肌與腹肌的快速神經徵召，將上肢拉力轉化為馬拉松上坡衝刺時的有節奏推進動能。",
    "tag": "#MedBallSlam"
  },
  {
    "id": 223,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Lateral Raise Tempo & Shoulder Girdle Armor",
    "en": "Slow eccentric lateral dumbbell raises condition the medial deltoids to withstand centrifugal forces during fast road racing turns and downhill switchbacks.",
    "zh": "慢速離心啞鈴側平舉能鍛鍊三角肌中束，承受公路賽快速急轉彎與盤山公路下坡折返跑時巨大的離心橫向剪力。",
    "tag": "#LateralRaise"
  },
  {
    "id": 224,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Push-to-Pull Balance & Rotator Cuff Protection",
    "en": "Adhering strictly to a two-to-one pulling-to-pushing training ratio protects runners from anterior shoulder instability and ensures unrestricted rib cage breathing mechanics.",
    "zh": "嚴格遵循二比一的拉力對推力重訓比例，能保護跑者免於前肩不穩定性，並確保胸廓肋骨呼吸力學暢通無阻。",
    "tag": "#PushPullRatio"
  },
  {
    "id": 225,
    "cat_id": "upper",
    "cat_zh": "上肢肌力與防護",
    "injury": "Upper Body Strength Reserve & Marathon Economy",
    "en": "Upper body resistance training elevates running economy by reducing excessive torso oscillation, allowing every watt of metabolic power to be directed purely forward.",
    "zh": "上肢阻力重訓能減少跑步中過度的軀幹橫向晃動，大幅提升跑步經濟性，使每一瓦特的代謝能量都能全數專注導向正前方。",
    "tag": "#RunningEconomy"
  }
];
