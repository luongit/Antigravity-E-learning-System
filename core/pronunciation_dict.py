"""
core/pronunciation_dict.py
Từ điển chuẩn hóa phát âm và phiên âm thuật ngữ bài giảng E-Learning.
Tổ chức theo các lĩnh vực:
1. Cơ quan - Danh từ riêng & Chức danh
2. Thuật ngữ Công nghệ Thông tin & Lập trình
3. Trí tuệ Nhân tạo (AI) - Khoa học Dữ liệu - Robotics
4. Giáo dục - Đào tạo - E-Learning
5. Kinh doanh - Quản trị - Khởi nghiệp
6. Marketing - Digital Marketing
7. Truyền thông đa phương tiện - Thiết kế - Video
8. Tên loại văn bản pháp quy
9. Cấp học, bằng cấp & Thuật ngữ giáo dục Việt Nam
10. Ký hiệu toán học & Lập trình
11. Đơn vị đo lường
12. Định dạng ngày tháng, giờ giấc
13. Nền tảng & Công cụ phổ biến
"""

import re
from typing import List, Tuple, Dict

# 1. Cơ quan - Danh từ riêng & Chức danh (Ưu tiên khớp cụm từ dài trước)
ORGANIZATION_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bBUNI-AI01\b", "bu ni ây ai không một", False),
    (r"\bBUNI-AI02\b", "bu ni ây ai không hai", False),
    (r"\bBUNI-AI03\b", "bu ni ây ai không ba", False),
    (r"\bBUNI-AI04\b", "bu ni ây ai không bốn", False),
    (r"\bBUNI-AI(\d+)\b", r"bu ni ây ai \1", False),
    (r"\bBUNI\b", "bu ni", False),
    (r"\bCTHĐQT\b", "Chủ tịch Hội đồng Quản trị", True),
    (r"\bHĐQT\b", "Hội đồng Quản trị", True),
    (r"\bHĐTV\b", "Hội đồng Thành viên", True),
    (r"\bBKS\b", "Ban Kiểm soát", True),
    (r"\bPTGĐ\b", "Phó Tổng Giám đốc", True),
    (r"\bTGĐ\b", "Tổng Giám đốc", True),
    (r"\bPGĐ\b", "Phó Giám đốc", True),
    (r"\bGĐ\b", "Giám đốc", True),
    (r"\bTNHH\b", "trách nhiệm hữu hạn", False),
    (r"\bCTCP\b", "công ty cổ phần", False),
    (r"\bTTg\b", "Thủ tướng Chính phủ", True),
    (r"\bTW\b", "Trung ương", True),
    (r"\bUBTVQH\b", "Ủy ban Thường vụ Quốc hội", True),
    (r"\bUBND\b", "Ủy ban nhân dân", True),
    (r"\bHĐND\b", "Hội đồng nhân dân", True),
    (r"\bQH\b", "Quốc hội", True),
    (r"\bBộ GD&ĐT\b", "Bộ Giáo dục và Đào tạo", False),
    (r"\bSở GD&ĐT\b", "Sở Giáo dục và Đào tạo", False),
    (r"\bPhòng GD&ĐT\b", "Phòng Giáo dục và Đào tạo", False),
    (r"\bBGDĐT\b", "Bộ Giáo dục và Đào tạo", True),
    (r"\bSGDĐT\b", "Sở Giáo dục và Đào tạo", True),
    (r"\bPGDĐT\b", "Phòng Giáo dục và Đào tạo", True),
    (r"\bGDĐT\b", "Giáo dục và Đào tạo", True),
    (r"\bBTTTT\b", "Bộ Thông tin và Truyền thông", True),
    (r"\bBKHCN\b", "Bộ Khoa học và Công nghệ", True),
    (r"\bBTC\b", "Bộ Tài chính", True),
    (r"\bBCA\b", "Bộ Công an", True),
    (r"\bBNV\b", "Bộ Nội vụ", True),
    (r"\bBYT\b", "Bộ Y tế", True),
    (r"\bBTP\b", "Bộ Tư pháp", True),
    (r"\bBLĐTBXH\b", "Bộ Lao động, Thương binh và Xã hội", True),
]

# 2. Thuật ngữ CNTT & Lập trình
IT_DEV_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bApplied AI for Information Technology\b", "áp plai ây ai pho in phô mêi sần tếch nơ lơ di", False),
    (r"\bCareer Passport\b", "Ca ri ơ Pát pọt", False),
    (r"\bEnterprise Capstone\b", "en tơ prai kép xtôn", False),
    (r"\bCapstone\b", "kép xtôn", False),
    (r"\bPortfolio\b", "pót phô li ô", False),
    (r"\bWeb Full Stack\b", "uép phun stack", False),
    (r"\bFull Stack\b", "phun stack", False),
    (r"\bSpring Boot\b", "sờ pơ ring bót", False),
    (r"\bReactJS\b", "ri ác giây ét", False),
    (r"\bFlutter\b", "phơ lắt tơ", False),
    (r"\bDart\b", "đát", False),
    (r"\bFrontEnd\b", "phờ rân en", False),
    (r"\bBackEnd\b", "bách en", False),
    (r"\bn8n\b", "en tám en", False),
    (r"\bAptech\b", "Áp tếch", False),
    (r"\bBachkhoa\b", "Bách Khoa", False),
    (r"\biOS\b", "ai ô ét", False),
    (r"\bAndroid\b", "an roi", False),
    (r"\bMô-đun\b", "mô đun", False),
    (r"\bmô-đun\b", "mô đun", False),
    (r"\bVideo\b", "vi đê ô", False),
    (r"\bdemo\b", "đê-mô", False),
    (r"\bFull Table Scan\b", "Phun thây bồ xờ ken", False),
    (r"\bDivide & Conquer\b", "Chia để trị", False),
    (r"\bDivide and Conquer\b", "Chia để trị", False),
    (r"\bRoot Cause Analysis\b", "phân tích nguyên nhân gốc rễ", False),
    (r"\bRoot Cause\b", "nguyên nhân gốc rễ", False),
    (r"\bMemory Overflow\b", "tràn bộ nhớ", False),
    (r"\bOut of Memory\b", "hết bộ nhớ", False),
    (r"\bMemory Leak\b", "rò rỉ bộ nhớ Me-mo-ry lích", False),
    (r"\bRESTful API\b", "rést phồ ây pi ai", False),
    (r"\bREST API\b", "rést ây pi ai", False),
    (r"\bSQL Server\b", "ét quy eo sơ-vờ", False),
    (r"\bSQL Query\b", "truy vấn ét quy eo", False),
    (r"\bSQL Index\b", "chỉ mục ét quy eo", False),
    (r"\bIndex SQL\b", "chỉ mục ét quy eo", False),
    (r"\bNoSQL\b", "nô ét quy eo", False),
    (r"\bMySQL\b", "mai ét quy eo", False),
    (r"\bPostgreSQL\b", "pốt gờ-rét ét quy eo", False),
    (r"\bMongoDB\b", "mon gô đi bi", False),
    (r"\bDatabase\b", "đây tờ bây-s", False),
    (r"\bDBMS\b", "đi bi em ét", True),
    (r"\bPull Request\b", "pun ri-quét", False),
    (r"\bFull-stack\b", "phun sờ-téc", False),
    (r"\bASP\.NET\b", "ây ét pi đót nét", False),
    (r"\b\.NET\b", "đót nét", False),
    (r"\bNode\.js\b", "nốt chấm giây ét", False),
    (r"\bVue\.js\b", "viu chấm giây ét", False),
    (r"\bTypeScript\b", "tai-p sờ cờ-ríp", False),
    (r"\bJavaScript\b", "gia va sờ cờ-ríp", False),
    (r"\bBrute-force\b", "bơ rút-phoóc", False),
    (r"\bIntegration Test\b", "in-tờ-grây-sần tét", False),
    (r"\bUnit Test\b", "iu-nịt tét", False),
    (r"\bTest case\b", "tét kây-s", False),
    (r"\bTest-case\b", "tét kây-s", False),
    (r"\b5 Whys\b", "5 Lần Tại Sao", False),
    (r"\bIshikawa\b", "Í-si-ka-oa", False),
    (r"\bAction Challenge\b", "Thách thức hành động", False),
    (r"\bChecklist\b", "chếch-lít", False),
    (r"\bCase study\b", "kết xì ta-đi", False),
    (r"\bFile log\b", "phai lốc", False),
    (r"\bLog file\b", "lốc phai", False),
    (r"\bCode dump\b", "cốt đăm", False),
    (r"\bFlowchart\b", "phờ-lâu chát", False),
    (r"\bFlowcharts\b", "phờ-lâu chát", False),
    (r"\bPseudocode\b", "mã giả su đô cốt", False),
    (r"\bSyntax\b", "xin-tắc", False),
    (r"\bVariable\b", "ve ri ờ bồ", False),
    (r"\bFunction\b", "phâng-sần", False),
    (r"\bParameter\b", "pờ-ra-mơ-tờ", False),
    (r"\bArgument\b", "a-giu-mần", False),
    (r"\bArray\b", "ờ-rây", False),
    (r"\bObject\b", "óp-jẹct", False),
    (r"\bClass\b", "cờ-lát", False),
    (r"\bInterface\b", "in-tờ-phâys", False),
    (r"\bBoolean\b", "bu-li-ần", False),
    (r"\bString\b", "sờ-trinh", False),
    (r"\bInteger\b", "in-ti-jờ", False),
    (r"\bFloat\b", "phờ-lốt", False),
    (r"\bDebugging\b", "đi-bấc-ghinh", False),
    (r"\bDebugger\b", "đi-bấc-gờ", False),
    (r"\bDebug\b", "đi-bấc", False),
    (r"\bBugs\b", "bấc", False),
    (r"\bBug\b", "bấc", False),
    (r"\bError\b", "e-rờ", False),
    (r"\bException\b", "éc-sep-sần", False),
    (r"\bRuntime\b", "ran-tai-m", False),
    (r"\bCompiler\b", "cơm-pai-lờ", False),
    (r"\bCompile\b", "cơm-pai-l", False),
    (r"\bLogs\b", "lốc", False),
    (r"\bLog\b", "lốc", False),
    (r"\bCache\b", "két-sh", False),
    (r"\bCookie\b", "cu-ki", False),
    (r"\bSession\b", "se-sần", False),
    (r"\bToken\b", "tô-kần", False),
    (r"\bTesting\b", "tét-ting", False),
    (r"\bTest\b", "tét", False),
    (r"\bSymptom\b", "triệu chứng bề mặt", False),
    (r"\bFramework\b", "phờ-rêm-uớc", False),
    (r"\bLibrary\b", "lai bờ re ri", False),
    (r"\bModule\b", "mo đun", False),
    (r"\bPackage\b", "péc-kịt", False),
    (r"\bPlugin\b", "plấc-in", False),
    (r"\bExtension\b", "éc-sten-sần", False),
    (r"\bAlgorithm\b", "an gờ-rít-thầm", False),
    (r"\bKubernetes\b", "ku bơ nét ti-s", False),
    (r"\bDocker\b", "đóc-cờ", False),
    (r"\bBackend\b", "bách en", False),
    (r"\bFrontend\b", "phờ-rân en", False),
    (r"\bClient\b", "cờ-lai-ần", False),
    (r"\bServer\b", "sơ-vờ", False),
    (r"\bCloud\b", "cờ-lao-đ", False),
    (r"\bGitHub\b", "gít hắp", False),
    (r"\bGitLab\b", "gít láp", False),
    (r"\bGit\b", "gít", False),
    (r"\bCommit\b", "cờ mít", False),
    (r"\bPush\b", "pút", False),
    (r"\bPull\b", "pun", False),
    (r"\bBranch\b", "branh-ch", False),
    (r"\bMerge\b", "mơ-j", False),
    (r"\bRepository\b", "ri pô zi to ri", False),
    (r"\bRepo\b", "ri pô", False),
    (r"\bTCP/IP\b", "ti xi pi, ai pi", False),
    (r"\bHTTPS\b", "hát ti ti pi ét", False),
    (r"\bHTTP\b", "hát ti ti pi", False),
    (r"\bJSON\b", "giây sần", False),
    (r"\bHTML\b", "hát ti em eo", False),
    (r"\bCSS\b", "xi ét ét", False),
    (r"\bXML\b", "éc em eo", False),
    (r"\bCSV\b", "xi ét vi", False),
    (r"\bYAML\b", "ya-mồ", False),
    (r"\bURL\b", "iu a eo", True),
    (r"\bURI\b", "iu a ai", True),
    (r"\bDNS\b", "đi en ét", True),
    (r"\bSSH\b", "ét ét hát", True),
    (r"\bSSL\b", "ét ét eo", True),
    (r"\bTLS\b", "ti eo ét", True),
    (r"\bVPN\b", "vi pi en", True),
    (r"\bUI/UX\b", "iu ai, iu éc", False),
    (r"\bUI\b", "iu ai", True),
    (r"\bUX\b", "iu éc", True),
    (r"\bSDK\b", "ét đi cây", True),
    (r"\bIDE\b", "ai đi i", True),
    (r"\bCLI\b", "xi eo ai", True),
    (r"\bGUI\b", "gu-i", True),
    (r"\bAPI\b", "ây pi ai", True),
    (r"\bCPU\b", "xi pi iu", True),
    (r"\bGPU\b", "gi pi iu", True),
    (r"\bRAM\b", "ram", True),
    (r"\bROM\b", "rom", True),
    (r"\bSSD\b", "ét ét đi", True),
    (r"\bHDD\b", "hát đi đi", True),
    (r"\bUSB\b", "iu ét bi", True),
    (r"\bIoT\b", "ai ô ti", False),
    (r"\bICT\b", "ai xi ti", True),
    (r"\bIT\b", "ai ti", True),
    (r"\bQA\b", "kiu ây", True),
    (r"\bQC\b", "kiu xi", True),
    (r"\bSQL\b", "ét quy eo", True),
    (r"\bPython\b", "pai thần", False),
    (r"\bJava\b", "gia va", False),
    (r"\bReact\b", "ri ác", False),
    (r"\bAngular\b", "eng giu lờ", False),
    (r"\bPHP\b", "pi hát pi", True),
    (r"\bC\+\+\b", "xi cộng cộng", True),
    (r"\bC#\b", "xi-sharp", True),
    (r"\bApp\b", "áp", False),
]

# 3. AI - Data Science - Robotics
AI_DATA_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bPrompt Engineering\b", "kỹ thuật thiết kế prôm", False),
    (r"\bComputer Vision\b", "cơm piu tờ vi dần", False),
    (r"\bVector Database\b", "cơ sở dữ liệu véc-tơ", False),
    (r"\bData Science\b", "đây tờ sai-ần-s", False),
    (r"\bData Scientist\b", "đây tờ sai-ần-tịt", False),
    (r"\bData Analytics\b", "đây tờ a-na-li-tích", False),
    (r"\bBig Data\b", "bích đây tờ", False),
    (r"\bDataset\b", "đây tờ sét", False),
    (r"\bData\b", "đây tờ", False),
    (r"\bMachine Learning\b", "mờ shin lơ ning", False),
    (r"\bDeep Learning\b", "đíp lơ ning", False),
    (r"\bGenerative AI\b", "jen nơ rây tiv ây ai", False),
    (r"\bGenAI\b", "jen ây ai", False),
    (r"\bAI Agent\b", "ây ai ây-jần", False),
    (r"\bAI Model\b", "mô hình ây ai", False),
    (r"\bAI\b", "ây ai", True),
    (r"\bA\.I\.\b", "ây ai", False),
    (r"\bLLM\b", "eo eo em", True),
    (r"\bNLP\b", "en eo pi", True),
    (r"\bML\b", "em eo", True),
    (r"\bNeural Network\b", "mạng nơ ron", False),
    (r"\bCNN\b", "xi en en", True),
    (r"\bRNN\b", "a en en", True),
    (r"\bTransformer\b", "tran-s-phoóc-mờ", False),
    (r"\bTensorFlow\b", "ten-sờ phờ-lâu", False),
    (r"\bTensor\b", "ten-sờ", False),
    (r"\bPyTorch\b", "pai toóc", False),
    (r"\bOpenCV\b", "ô-pần xi vi", False),
    (r"\bPrompt\b", "prôm", False),
    (r"\bChatbot\b", "chát-bót", False),
    (r"\bAgent\b", "ây-jần", False),
    (r"\bRAG\b", "rác", True),
    (r"\bEmbedding\b", "em-be-đinh", False),
    (r"\bVector\b", "véc-tơ", False),
    (r"\bConfusion Matrix\b", "ma trận nhầm lẫn", False),
    (r"\bF1-score\b", "điểm ép một", False),
    (r"\bRaspberry Pi\b", "ráp-bờ-ri pai", False),
    (r"\bArduino\b", "a-đu-i-nô", False),
    (r"\bMicrocontroller\b", "vi điều khiển", False),
    (r"\bActuator\b", "cơ cấu chấp hành", False),
    (r"\bRobotics\b", "rô-bó-tích", False),
    (r"\bRobot\b", "rô-bốt", False),
]

# 4. Giáo dục - Đào tạo - E-Learning
EDUCATION_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bEducation Technology\b", "công nghệ giáo dục", False),
    (r"\bLearning Outcome\b", "chuẩn đầu ra", False),
    (r"\bLearning Objectives\b", "mục tiêu học tập", False),
    (r"\bBlended Learning\b", "học tập kết hợp", False),
    (r"\bHybrid Learning\b", "học tập kết hợp trực tiếp và trực tuyến", False),
    (r"\bMultiple Choice\b", "trắc nghiệm nhiều lựa chọn", False),
    (r"\bE-Learning\b", "i lơ ning", False),
    (r"\beLearning\b", "i lơ ning", False),
    (r"\bLCMS\b", "eo xi em ét", True),
    (r"\bLMS\b", "eo em ét", True),
    (r"\bMOOC\b", "múc", True),
    (r"\bSCORM\b", "sờ-coóc-m", False),
    (r"\bxAPI\b", "éc ây pi ai", False),
    (r"\bEdTech\b", "ét-téc", False),
    (r"\bSTEAM\b", "sti-m", True),
    (r"\bSTEM\b", "stem", True),
    (r"\bMicrolearning\b", "học tập vi mô", False),
    (r"\bSelf-learning\b", "tự học", False),
    (r"\bRubric\b", "bảng tiêu chí đánh giá", False),
]

# 5. Kinh doanh - Quản trị - Khởi nghiệp
BUSINESS_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bBusiness Model Canvas\b", "mô hình kinh doanh canvas", False),
    (r"\bBusiness Model\b", "mô hình kinh doanh", False),
    (r"\bBusiness Plan\b", "kế hoạch kinh doanh", False),
    (r"\bCustomer Segment\b", "phân khúc khách hàng", False),
    (r"\bBreak-even Point\b", "điểm hòa vốn", False),
    (r"\bGross Profit\b", "lợi nhuận gộp", False),
    (r"\bNet Profit\b", "lợi nhuận ròng", False),
    (r"\bTarget Market\b", "thị trường mục tiêu", False),
    (r"\bTarget Customer\b", "khách hàng mục tiêu", False),
    (r"\bMarket Share\b", "thị phần", False),
    (r"\bCash Flow\b", "dòng tiền", False),
    (r"\bBest Practice\b", "thực tiễn tốt", False),
    (r"\bBenchmark\b", "đối chuẩn", False),
    (r"\bCo-founder\b", "đồng sáng lập", False),
    (r"\bFounder\b", "nhà sáng lập", False),
    (r"\bStartup\b", "khởi nghiệp", False),
    (r"\bStakeholder\b", "bên liên quan", False),
    (r"\bShareholder\b", "cổ đông", False),
    (r"\bRoadmap\b", "lộ trình", False),
    (r"\bMilestone\b", "cột mốc", False),
    (r"\bPESTEL\b", "pét-tồ", True),
    (r"\bPEST\b", "pét", True),
    (r"\bSWOT\b", "sờ-uốt", True),
    (r"\bBMC\b", "bi em xi", True),
    (r"\bKPI's\b", "các cây pi ai", False),
    (r"\bKPIs\b", "các cây pi ai", False),
    (r"\bKPI\b", "cây pi ai", True),
    (r"\bOKR\b", "ô cây a", True),
    (r"\bROI\b", "a ô ai", True),
    (r"\bROE\b", "a ô i", True),
    (r"\bROA\b", "a ô ây", True),
    (r"\bB2B\b", "bi tu bi", False),
    (r"\bB2C\b", "bi tu xi", False),
    (r"\bC2C\b", "xi tu xi", False),
    (r"\bB2G\b", "bi tu gi", False),
    (r"\bD2C\b", "đi tu xi", False),
    (r"\bCRM\b", "xi a em", True),
    (r"\bERP\b", "i a pi", True),
    (r"\bHRM\b", "hát a em", True),
    (r"\bHR\b", "hát a", True),
    (r"\bSaaS\b", "sát", False),
    (r"\bPaaS\b", "pát", False),
    (r"\bIaaS\b", "ai át", False),
    (r"\bCEO\b", "xi i ô", True),
    (r"\bCFO\b", "xi ép ô", True),
    (r"\bCTO\b", "xi ti ô", True),
    (r"\bCOO\b", "xi ô ô", True),
    (r"\bCMO\b", "xi em ô", True),
    (r"\bCIO\b", "xi ai ô", True),
    (r"\bCHRO\b", "xi hát a ô", True),
]

# 6. Marketing - Digital Marketing
MARKETING_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bAffiliate Marketing\b", "tiếp thị liên kết", False),
    (r"\bAffiliate\b", "a-phi-li-ợt", False),
    (r"\bDigital Marketing\b", "đi-gi-tồ ma-kờ-ting", False),
    (r"\bContent Marketing\b", "con-ten ma-kờ-ting", False),
    (r"\bMarketing\b", "ma-kờ-ting", False),
    (r"\bBrand Awareness\b", "nhận biết thương hiệu", False),
    (r"\bOrganic Traffic\b", "lưu lượng truy cập tự nhiên", False),
    (r"\bLanding Page\b", "trang đích", False),
    (r"\bConversion Rate\b", "tỷ lệ chuyển đổi", False),
    (r"\bFlash Sale\b", "phờ-lét xeo", False),
    (r"\bLivestream\b", "lai-v sờ-trim", False),
    (r"\bInfluencer\b", "in-phờ-lu-en-sờ", False),
    (r"\bVoucher\b", "vao-chờ", False),
    (r"\bCoupon\b", "cu-pon", False),
    (r"\bSEO\b", "ét i ô", True),
    (r"\bSEM\b", "ét i em", True),
    (r"\bSMM\b", "ét em em", True),
    (r"\bPPC\b", "pi pi xi", True),
    (r"\bCPC\b", "xi pi xi", True),
    (r"\bCPM\b", "xi pi em", True),
    (r"\bCPA\b", "xi pi ây", True),
    (r"\bCTR\b", "xi ti a", True),
    (r"\bCTA\b", "xi ti ây", True),
    (r"\bCPL\b", "xi pi eo", True),
    (r"\bKOL\b", "cây ô eo", True),
    (r"\bKOC\b", "cây ô xi", True),
]

# 7. Truyền thông đa phương tiện - Thiết kế - Video
MEDIA_DESIGN_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bMotion Graphic\b", "đồ họa chuyển động", False),
    (r"\bGraphic Design\b", "thiết kế đồ họa", False),
    (r"\bDigital Media\b", "đi-gi-tồ mi-đi-a", False),
    (r"\bMultimedia\b", "mân-ti-mi-đi-a", False),
    (r"\bAfter Effects\b", "áp-tờ i-phéc", False),
    (r"\bPhotoshop\b", "phô-tô-sóp", False),
    (r"\bIllustrator\b", "i-lớt-trây-tờ", False),
    (r"\bInDesign\b", "in-đi-zai-n", False),
    (r"\bLightroom\b", "lai-t rum", False),
    (r"\bPremiere\b", "pờ-ri-mia", False),
    (r"\bFull HD\b", "phun hát đi", False),
    (r"\bCapCut\b", "cáp-cắt", False),
    (r"\bCanva\b", "can-va", False),
    (r"\bFigma\b", "phích-ma", False),
    (r"\bFrame Rate\b", "tốc độ khung hình", False),
    (r"\bAnimation\b", "hoạt hình", False),
    (r"\bRendering\b", "ren-đờ-rinh", False),
    (r"\bRender\b", "ren-đờ", False),
    (r"\bKeyframe\b", "ki-phờ-rêm", False),
    (r"\bVoice-over\b", "lời thuyết minh", False),
    (r"\bSubtitle\b", "phụ đề", False),
    (r"\bTimeline\b", "tai-m-lai-n", False),
    (r"\bMegapixel\b", "mê-ga-pích-xeo", False),
    (r"\bPixel\b", "pích-xeo", False),
    (r"\bFPS\b", "ép pi ét", True),
    (r"\bCMYK\b", "xi em oai cây", True),
    (r"\bRGB\b", "a gi bi", True),
    (r"\bDPI\b", "đi pi ai", True),
    (r"\b4K\b", "bốn cây", False),
    (r"\b8K\b", "tám cây", False),
    (r"\bHD\b", "hát đi", True),
    (r"\b3D\b", "ba đi", False),
    (r"\b2D\b", "hai đi", False),
]

# 8. Tên loại văn bản quy phạm pháp luật
LEGAL_DOC_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bQĐ-BGDĐT\b", "Quyết định của Bộ Giáo dục và Đào tạo", True),
    (r"\bQĐ-TTg\b", "Quyết định của Thủ tướng Chính phủ", True),
    (r"\bTT-BLĐTBXH\b", "Thông tư của Bộ Lao động, Thương binh và Xã hội", True),
    (r"\bTT-BGDĐT\b", "Thông tư của Bộ Giáo dục và Đào tạo", True),
    (r"\bTT-BTTTT\b", "Thông tư của Bộ Thông tin và Truyền thông", True),
    (r"\bTT-BKHCN\b", "Thông tư của Bộ Khoa học và Công nghệ", True),
    (r"\bTT-BTC\b", "Thông tư của Bộ Tài chính", True),
    (r"\bTT-BNV\b", "Thông tư của Bộ Nội vụ", True),
    (r"\bNĐ-CP\b", "Nghị định của Chính phủ", True),
    (r"\bNQ-CP\b", "Nghị quyết của Chính phủ", True),
    (r"\bNQ/TW\b", "Nghị quyết Trung ương", True),
    (r"\bCT-TTg\b", "Chỉ thị của Thủ tướng Chính phủ", True),
    (r"\bNĐ\b", "Nghị định", True),
    (r"\bQĐ\b", "Quyết định", True),
    (r"\bTT\b", "Thông tư", True),
    (r"\bNQ\b", "Nghị quyết", True),
    (r"\bCT\b", "Chỉ thị", True),
]

# 9. Cấp học, bằng cấp & Thuật ngữ giáo dục Việt Nam
VN_EDU_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bCTGDPT 2018\b", "Chương trình Giáo dục phổ thông năm 2018", True),
    (r"\bCTGDPT\b", "Chương trình Giáo dục phổ thông", True),
    (r"\bGDPT\b", "giáo dục phổ thông", True),
    (r"\bTHCS\b", "trung học cơ sở", True),
    (r"\bTHPT\b", "trung học phổ thông", True),
    (r"\bGDTX\b", "giáo dục thường xuyên", True),
    (r"\bGDNN\b", "giáo dục nghề nghiệp", True),
    (r"\bCBQLGD\b", "cán bộ quản lý giáo dục", True),
    (r"\bCBQL\b", "cán bộ quản lý", True),
    (r"\bCBGV\b", "cán bộ giáo viên", True),
    (r"\bGVBM\b", "giáo viên bộ môn", True),
    (r"\bGVCN\b", "giáo viên chủ nhiệm", True),
    (r"\bPPDH\b", "phương pháp dạy học", True),
    (r"\bKT-ĐG\b", "kiểm tra, đánh giá", True),
    (r"\bKTĐG\b", "kiểm tra đánh giá", True),
    (r"\bCNTT\b", "công nghệ thông tin", True),
    (r"\bCĐS\b", "chuyển đổi số", True),
    (r"\bNLS\b", "năng lực số", True),
    (r"\bMN\b", "mầm non", True),
    (r"\bTH\b", "tiểu học", True),
    (r"\bĐH\b", "đại học", True),
    (r"\bCĐ\b", "cao đẳng", True),
    (r"\bTC\b", "trung cấp", True),
    (r"\bGV\b", "giáo viên", True),
    (r"\bHS\b", "học sinh", True),
    (r"\bSV\b", "sinh viên", True),
    (r"\bHV\b", "học viên", True),
]

# 10. Ký hiệu lập trình & Toán học logic
MATH_CODE_SYMBOLS: List[Tuple[str, str, bool]] = [
    (r"===", "bằng bằng bằng", False),
    (r"==", "bằng bằng", False),
    (r"!==", "khác bằng bằng", False),
    (r"!=", "khác bằng", False),
    (r">=", "lớn hơn hoặc bằng", False),
    (r"<=", "nhỏ hơn hoặc bằng", False),
    (r"≥", "lớn hơn hoặc bằng", False),
    (r"≤", "nhỏ hơn hoặc bằng", False),
    (r"≠", "khác", False),
    (r"\+\+", "cộng cộng", False),
    (r"--", "trừ trừ", False),
    (r"\+=", "cộng bằng", False),
    (r"-=", "trừ bằng", False),
    (r"=>", "mũi tên", False),
    (r"&&", " và ", False),
    (r"\|\|", " hoặc ", False),
    (r"°C\b", "độ C", False),
    (r"°F\b", "độ F", False),
    (r"‰", " phần nghìn", False),
    (r"±", " cộng hoặc trừ ", False),
    (r"≈", " xấp xỉ ", False),
    (r"∞", " vô cực ", False),
    (r"√", " căn bậc hai ", False),
    (r"π", " pi ", False),
    (r"Δ", " đen-ta ", False),
    (r"Σ", " xích-ma ", False),
    (r"×", " nhân ", False),
    (r"÷", " chia ", False),
]

# 11. Đơn vị đo lường (Kèm tiền tố số học)
UNIT_TERMS: List[Tuple[str, str, bool]] = [
    (r"(\d+)\s*mm²\b", r"\1 mi-li-mét vuông", False),
    (r"(\d+)\s*cm²\b", r"\1 xen-ti-mét vuông", False),
    (r"(\d+)\s*m²\b", r"\1 mét vuông", False),
    (r"(\d+)\s*km²\b", r"\1 ki-lô-mét vuông", False),
    (r"(\d+)\s*cm³\b", r"\1 xen-ti-mét khối", False),
    (r"(\d+)\s*m³\b", r"\1 mét khối", False),
    (r"(\d+)\s*kWh\b", r"\1 ki-lô-oát giờ", False),
    (r"(\d+)\s*Wh\b", r"\1 oát giờ", False),
    (r"(\d+)\s*kW\b", r"\1 ki-lô-oát", False),
    (r"(\d+)\s*W\b", r"\1 oát", True),
    (r"(\d+)\s*GHz\b", r"\1 gi-ga-héc", False),
    (r"(\d+)\s*MHz\b", r"\1 mê-ga-héc", False),
    (r"(\d+)\s*kHz\b", r"\1 ki-lô-héc", False),
    (r"(\d+)\s*Hz\b", r"\1 héc", False),
    (r"(\d+)\s*Gbps\b", r"\1 gi-ga-bít trên giây", False),
    (r"(\d+)\s*Mbps\b", r"\1 mê-ga-bít trên giây", False),
    (r"(\d+)\s*TB\b", r"\1 tê-ra-bai", True),
    (r"(\d+)\s*GB\b", r"\1 gi-ga-bai", True),
    (r"(\d+)\s*MB\b", r"\1 mê-ga-bai", True),
    (r"(\d+)\s*KB\b", r"\1 ki-lô-bai", True),
    (r"(\d+)\s*mV\b", r"\1 mi-li-vôn", False),
    (r"(\d+)\s*V\b", r"\1 vôn", True),
    (r"(\d+)\s*mA\b", r"\1 mi-li-am-pe", False),
    (r"(\d+)\s*A\b", r"\1 am-pe", True),
    (r"(\d+)\s*mg\b", r"\1 mi-li-gam", False),
    (r"(\d+)\s*kg\b", r"\1 ki-lô-gam", False),
    (r"(\d+)\s*g\b", r"\1 gam", True),
    (r"(\d+)\s*ml\b", r"\1 mi-li-lít", False),
    (r"(\d+)\s*mL\b", r"\1 mi-li-lít", False),
    (r"(\d+)\s*l\b", r"\1 lít", True),
    (r"(\d+)\s*L\b", r"\1 lít", True),
    (r"(\d+)\s*mm\b", r"\1 mi-li-mét", False),
    (r"(\d+)\s*cm\b", r"\1 xen-ti-mét", False),
    (r"(\d+)\s*km\b", r"\1 ki-lô-mét", False),
    (r"(\d+)\s*m\b", r"\1 mét", True),
]

# 12. Tên Nền tảng & Công cụ phổ biến
PLATFORM_TERMS: List[Tuple[str, str, bool]] = [
    (r"\bGoogle Classroom\b", "gu-gồ cờ-lát-rum", False),
    (r"\bGoogle Drive\b", "gu-gồ đờ-rai-v", False),
    (r"\bGoogle Docs\b", "gu-gồ đốc", False),
    (r"\bGoogle Sheets\b", "gu-gồ sít", False),
    (r"\bGoogle Meet\b", "gu-gồ mít", False),
    (r"\bGoogle\b", "gu-gồ", False),
    (r"\bMicrosoft Teams\b", "mai-cờ-rô-sóp tim", False),
    (r"\bMicrosoft\b", "mai-cờ-rô-sóp", False),
    (r"\bPowerPoint\b", "pao-ờ-poi-n-t", False),
    (r"\bChatGPT\b", "chát gi pi ti", False),
    (r"\bYouTube\b", "iu-túp", False),
    (r"\bFacebook\b", "phây-s-búc", False),
    (r"\bTikTok\b", "tích-tóc", False),
    (r"\bInstagram\b", "in-stờ-gram", False),
    (r"\bLinkedIn\b", "lin-kờ-đin", False),
    (r"\bOpenAI\b", "ô-pần ây ai", False),
    (r"\bCopilot\b", "cô-pai-lợt", False),
    (r"\bGemini\b", "gem-mi-nai", False),
    (r"\bClaude\b", "cờ-lót", False),
    (r"\bWord\b", "uớt", False),
    (r"\bExcel\b", "éc-xeo", False),
]

# Tổng hợp tất cả các danh mục từ điển, sắp xếp theo độ dài mẫu giảm dần
_ALL_CATEGORIES = [
    LEGAL_DOC_TERMS,
    ORGANIZATION_TERMS,
    IT_DEV_TERMS,
    AI_DATA_TERMS,
    EDUCATION_TERMS,
    BUSINESS_TERMS,
    MARKETING_TERMS,
    MEDIA_DESIGN_TERMS,
    VN_EDU_TERMS,
    PLATFORM_TERMS,
]

# Gộp và sắp xếp theo độ dài pattern giảm dần (ưu tiên cụm dài trước cụm ngắn)
MASTER_PRONUNCIATION_LIST: List[Tuple[str, str, bool]] = []
for cat in _ALL_CATEGORIES:
    MASTER_PRONUNCIATION_LIST.extend(cat)

# Sắp xếp các cụm dài lên đầu
MASTER_PRONUNCIATION_LIST.sort(key=lambda item: len(item[0]), reverse=True)


def normalize_pronunciation(text: str) -> str:
    """
    Chuẩn hóa phát âm toàn diện theo từ điển cho văn bản đọc TTS:
    1. Xử lý ngày tháng, thời gian, tỉ lệ
    2. Xử lý ký hiệu toán học & đơn vị đo lường
    3. Thay thế thuật ngữ theo Master Dictionary (ưu tiên cụm dài)
    """
    if not text:
        return ""

    t = text

    # Chuẩn hóa Unicode dấu gạch ngang và ngoặc kép typographic
    t = t.replace("–", "-").replace("—", "-").replace("“", '"').replace("”", '"')
    t = t.replace("’", "'").replace("‘", "'").replace("…", "...")

    # Xử lý ngày tháng: (ngày )?DD/MM/YYYY -> ngày DD tháng MM năm YYYY
    t = re.sub(
        r"(?i)(?:ngày\s+)?\b(\d{1,2})[/](\d{1,2})[/](\d{4})\b",
        r"ngày \1 tháng \2 năm \3",
        t
    )
    # Xử lý ngày tháng: (ngày )?DD/MM -> ngày DD tháng MM (trừ tỉ lệ 24/7)
    t = re.sub(
        r"(?i)(?:ngày\s+)?\b(?!24/7)(\d{1,2})[/](\d{1,2})\b",
        r"ngày \1 tháng \2",
        t
    )
    # Tỉ lệ 24/7
    t = re.sub(r"\b24/7\b", "hai mươi bốn trên bảy", t)

    # Giờ giấc: 08:30 hoặc 8h30 -> 8 giờ 30 phút; 14h -> 14 giờ
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", r"\1 giờ \2 phút", t)
    t = re.sub(r"\b(\d{1,2})h(\d{2})\b", r"\1 giờ \2 phút", t)
    t = re.sub(r"\b(\d{1,2})h\b", r"\1 giờ", t)

    # Phần trăm: 50% -> 50 phần trăm
    t = re.sub(r"(\d+)\s*%", r"\1 phần trăm", t)

    # Đơn vị đo lường
    for pattern, repl, case_sensitive in UNIT_TERMS:
        flags = 0 if case_sensitive else re.IGNORECASE
        t = re.sub(pattern, repl, t, flags=flags)

    # Ký hiệu toán học logic
    for pattern, repl, case_sensitive in MATH_CODE_SYMBOLS:
        t = t.replace(pattern, repl)

    # Thay thế thuật ngữ theo từ điển chính
    for pattern, repl, case_sensitive in MASTER_PRONUNCIATION_LIST:
        flags = 0 if case_sensitive else re.IGNORECASE
        t = re.sub(pattern, repl, t, flags=flags)

    # Dọn dẹp khoảng trắng dư thừa
    t = re.sub(r"\s+", " ", t).strip()
    return t
