## merge_regi  
Windows XP registory Merge Python Scripts on ubuntu 20.04.  
  
PC: Ubuntu Mate 20.04  
  
#### 1. copy the WindowsXP Hiv file to work holder.    
    $ sudo mount -t ntfs /dev/sdb? /mnt/backup  
    $ copy /mnt/backup/WINDOWS/System32/config/system ./xp_system.new  
  
#### 2. edit merge_regi_nishi.py    
    change the following variables accroding to your env.  
    path='xp_system.new'    # hiv file path  
    reg_file="linux.reg"    # mergeide.reg  file path  use '/' letter in key  
    prefix = 'HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/'     # use '/' letter. don't use back slash  

#### 3. run compare check    
  
    change code      
      #mrg.merge()    
      mrg.comp_check()       
    
    $ python3 merge_regi_nishi.py    

#### 4. run merge    
    change code      
      mrg.merge()    
      #mrg.comp_check()       
   
    $ python3 merge_regi_nishi.py    

#### 5. save to Windows XP    
    $ copy /mnt/backup/WINDOWS/System32/config/system /mnt/backup/WINDOWS/System32/config/system.backup  
    $ copy ./xp_system.new /mnt/backup/WINDOWS/System32/config/system  
    $ sudo umount /mnt/backup  
