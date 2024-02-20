import BCSFE_Python_Discord as BCSFE_Python
import traceback
from BCSFE_Python_Discord import *

def downloadfile(tccode, cccode, country, gvcode):
        try:
            path = helper.save_file(
                "세이브 파일 저장",
                helper.get_save_file_filetype(),
                helper.get_save_path_home(),
            )
            BCSFE_Python.helper.set_save_path(path)
            country_code = country
            transfer_code = tccode
            confirmation_code = cccode
            game_version = gvcode
            game_version = helper.str_to_gv(game_version)
            try:
                save_data = BCSFE_Python.server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)
                save = 1
            except:
                print("기종변경 오류")
                save = 0
                pass
            if save == 1:
                save_data = patcher.patch_save_data(save_data, country_code)
                global save_stats
                save_stats = parse_save.start_parse(save_data, country_code)
                if save_stats == 0:
                    print("기종변경 오류")
                else:
                    
                    edits.save_management.save.save_save(save_stats)

                    print("세이브 로드 성공")
        except Exception as e:
            print(traceback.format_exc())
            
            pass
