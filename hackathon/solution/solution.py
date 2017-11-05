"""This module is main module for contestant's solution."""
 
from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir
 
 
def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
   
    if msg.current_load > 2.5: #ako krene da trosi vise
        if msg.solar_production-msg.current_load > 0 or msg.buying_price < 5: #proveravamo da li
            #panel proizvodi vise nego sto trosimo ili je jeftina struja
            #moze da bude ukljucen bojler...
            load3 = True
        else:
            #u drugom slucaju nikako
            load3 = False
    else:
        #ako ne divlja struja okej je da bude upaljen bojler i ako je skupa struja
        load3 = True
   
     #ako je skupa struja
    if msg.current_load > 7.0: # proverimo da li divlja ###### ovo sam promenio bilo je 7
        if msg.solar_production-msg.current_load > 0 : #ako divlja proveravamo da li proizvodimo
                #vise nego sto trosimo, okej je da bude upaljen u tom slucaju
            load2 = True
        else:
            #gasimo i to ako se ovo gore ne desi
            load2 = False
    else:
        #ako je jeftina struja moze da bude ukljucen
        load2 = True
   
   
    pr = calculatePowerReference(msg)
    
    if 7140 < msg.id <= 7200 and msg.bessSOC > 0 and msg.grid_status:
        
        loadSum = 0.2
        if load2:
            loadSum += 0.5
        if load3:
            loadSum += 0.3
            
            
        pr = loadSum * msg.current_load
        
        if pr > 6.0:
            pr = 6.0
        
        
        
    pv = calculatePV(msg)
    
    
    return ResultsMessage(data_msg=msg,
                          load_one=True,
                          load_two=load2,
                          load_three=load3,
                          power_reference = pr,
                          pv_mode = pv)
       
    # Dummy result is returned in every cycle here
 
 
def calculatePowerReference(msg : DataMessage):
    if msg.bessSOC != 1: #ako baterija nije puna
        if msg.solar_production > msg.current_load: #ako ako je proizvodnja panela veca od potraznje struje
            return (-1)*(msg.solar_production - msg.current_load) #puni bateriju sa viskom
    if msg.bessSOC < 0.20: #ako je ako je baterija 20% puna
        if not msg.grid_status:
            return (0.0)
        else:
            if msg.buying_price < 5:
                if msg.solar_production == 0:
                    return (-0.72)
                else:
                    if msg.solar_production < 6:
                        return ((-1) * msg.solar_production)
                    else:
                        return (-6.0)
            else:
                return (0.0)
    else:
        if not msg.grid_status:
            return (0.0)
        else:
            if msg.buying_price < 5:
                if msg.solar_production == 0:
                    return (-0.72)
                else:
                    if msg.solar_production < 6:
                        return ((-1) * msg.solar_production)
                    else:
                        return (-6.0)
            else:
                if (msg.current_load - msg.solar_production) <= 6.0:
                    return (msg.current_load - msg.solar_production)
                else:
                    return (6.0)
               
               
               
               
           
def calculatePV(msg : DataMessage):
    if not msg.grid_status and msg.bessSOC == 1.0:
        return (PVMode.OFF)
    else:
        return (PVMode.ON)
       
def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')
 
    cntrl = Control()
 
    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
        
        
# """This module is main module for contestant's solution."""
#  
# from hackathon.utils.control import Control
# from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
#     TYPHOON_DIR, config_outs
# from hackathon.framework.http_server import prepare_dot_dir
#  
#  
# def worker(msg: DataMessage) -> ResultsMessage:
#     """TODO: This function should be implemented by contestants."""
#     # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
#    
#     # Ako je trenutna potrosnja veca od 2.5
#     if msg.current_load > 2.5:
#         # i solarna proizvodnja veca od 2.5
#         if msg.solar_production - msg.current_load > 0:
#             # Upali LOAD3
#             load3 = True
#         else:
#             # U suprodnom ugasi LOAD3
#             load3 = False
#     else:
#         # Ako je trenutna potrosnja manja od 2.5 upali LOAD3
#         load3 = True
#    
#    
#     # Ako je trenutna potrosnja veca od 5.5
#     if msg.current_load > 6:
#         # i solarna proizvodnja je veca od 5.5
#         if msg.solar_production - msg.current_load > 0:
#             # Upali LOAD2
#             load2 = True
#         else:
#             # U suprotnom ugasi LOAD2
#             load2 = False
#     else:
#         # Ako je trenutna potrosnja manja od 5.5 upali LOAD2
#         load2 = True
#        
#     # Ako se baterija isprazni
#     if msg.bessSOC == 0:
#         # Ugasi LOAD1
#         load1 = False
#     else:
#         # U suprotnom neka LOAD1 radi
#         load1=True
#            
#     
#     pr = calculatePowerReference(msg)
#     pv = calculatePV(msg)
#     return ResultsMessage(data_msg=msg,
#                           load_one=load1,
#                           load_two=load2,
#                           load_three=load3,
#                           power_reference = pr,
#                           pv_mode = pv)
#        
#     # Dummy result is returned in every cycle here
#  
#  
# def calculatePowerReference(msg : DataMessage):
#     
#     '''
#         Funkcija koja izracunava kojom snagom punimo bateriju
#     
#     '''
#     
#     # Ako baterija nije napunjena
#     if msg.bessSOC < 1:
#         # I ako je solarna proizvodnja veca od trenutne potrosnje
#         if msg.solar_production > msg.current_load:
#             # Baterija treba da se puni viskom energije iz solarnog panela
#             return (-1)*(msg.solar_production - msg.current_load)
#     
#     # Ako je baterija na manje od 20%
#     if msg.bessSOC < 0.2:
#         # I nemamo struju
#         if not msg.grid_status:
#             # Ne punimo bateriju
#             return (0.0)
#         # Ako imamo struju
#         else:
#             # I ako je kupovna cena 3 (jeftina struja)
#             if msg.buying_price < 5:
#                 # I ako nemamo solarnu proizvodnju
#                 if msg.solar_production == 0:
#                     # Punimo bateriju lagano na jeftinoj struji
#                     return (-0.143)
#                 # U suprotnom ako imamo solarnu proizvodnju
#                 else:
#                     # I proizvodnja je manja od 6
#                     if msg.solar_production < 6:
#                         # Punimo bateriju tom solarnom enerijom
#                         return ((-1) * msg.solar_production)
#                     else:
#                         # Ako imamo solarnu proizvodnju vecu od 6, punimo bateriju maksimalnom brzinom
#                         return (-6.0)
#             # Ako je cena struje 8 (skupa struja) NE PUNIMO BATERIJU
#             else:
#                 return (0.0)
#     # Ako je baterija na vise od 20% 
#     else:
#         # I nemamo struju
#         if not msg.grid_status:
#             # Ne punimo bateriju
#             return (0.0)
#         else:
#             # Ako imamo struju i cena je 3 (jeftina struja)
#             if msg.buying_price < 5:
#                 # I ako nemamo solarnu proizvodnju
#                 if msg.solar_production == 0:
#                     # Punimo bateriju laganim intenzitetom
#                     return (-0.143)
#                 # Ako imamo solarnu proizvodnju
#                 else:
#                     # I ako je ona manja od 6
#                     if msg.solar_production < 6:
#                         # Punimo bateriju tom solarnom energijom
#                         return ((-1) * msg.solar_production)
#                     else:
#                         # Ako imamo solarnu proizvodnju vecu od 6, punimo bateriju maksimalnom brzinom
#                         return (-6.0)
#             # Ako je cena struje 8 (Skupa struja)
#             else:
#                 # I ako je prodajna cena 0 ne radimo nista
#                 if msg.selling_price == 0:
#                     return (0.0)
#                 # Ako je prodajna cena 3, praznimo bateriju
#                 else:
#                     return (6.0)
#            
# def calculatePV(msg : DataMessage):
#     
#     '''
#         Funkcija koja iskljucuje solarni panel u slucaju kada nemamo struju i baterija je puna
#         
#     '''
#     
#     if not msg.grid_status and msg.bessSOC == 1.0:
#         return (PVMode.OFF)
#     else:
#         return (PVMode.ON)
#        
#        
# def run(args) -> None:
#     prepare_dot_dir()
#     config_outs(args, 'solution')
#  
#     cntrl = Control()
#  
#     for data in cntrl.get_data():
#         cntrl.push_results(worker(data))