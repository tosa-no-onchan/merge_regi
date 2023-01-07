## merge_regi  
Windows XP registory Merge Python Scripts on ubuntu 20.04.  
  
PC: Ubuntu Mate 20.04  
  
#### 1. edit merge_regi_nishi.py  
 change the following variables accroding to your env.  
   path='xp_system.new'    # hiv file path  
   reg_file="linux.reg"    # mergeide.reg  file path  use '/' letter in key  
   prefix = 'HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/'     # use '/' letter. don't use back slash  

#### 2. run compare check  
  
  change code      
    #mrg.merge()    
    mrg.comp_check()       
   
  $ python3 merge_regi_nishi.py    

#### 3. run merge    
   change code      
    mrg.merge()    
    #mrg.comp_check()       
   
  $ python3 merge_regi_nishi.py    
