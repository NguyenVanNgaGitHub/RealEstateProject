import pandas as pd
data = pd.read_csv("../type_data.csv")
data = data[data["type"]!="UNKNOW"]

type_mapping = {
    "Nhà đất": ["Mua bán nhà riêng", "nhà trong hẻm", "Mua bán nhà phố", "nhà mặt tiền", "Nhà ở",
                "Mua bán nhà mặt phố", "Nhà riêng", "Nhà mặt phố"],
    "Đất nền": ["đất thổ cư, đất ở", "Đất", "đất nền, liền kề, đất dự án", "Mua bán đất", "Đất nền khu dân cư",
                "mặt bằng", "Đất nền", "Đất nền dự án", "Mua bán đất nền dự án"],
    "Căn hộ": ["Mua bán căn hộ chung cư", "Căn hộ/Chung cư", "căn hộ chung cư", "Căn hộ chung cư",
               "Căn hộ Cao cấp", "Căn hộ trung cấp", "Căn hộ mini", "Căn hộ Tập thể"],
    "Biệt thự": ["Mua bán biệt thự", "biệt thự, nhà liền kề", "Mua bán nhà biệt thự liền kề",
                 "Biệt thự liền kề", "Nhà biệt thự"],
    "Loại hình khác": ["Văn phòng, Mặt bằng kinh doanh", "kho, xưởng", "nhà hàng, khách sạn",
                       "đất nông, lâm nghiệp", "phòng trọ, nhà trọ", "Mua bán nhà hàng - khách sạn",
                       "Mua bán văn phòng", "trang trại", "Mua bán phòng trọ", "văn phòng",
                       "Mặt bằng bán lẻ", "các loại khác", "Mua bán trang trại khu nghỉ dưỡng"]
}

def get_refine_type(t):
    for x in type_mapping:
        if t in type_mapping[x]:
            return x
data["type"] = data["type"].apply(get_refine_type)
data.to_csv("../refine_type_data.csv", index=False)
