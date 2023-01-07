#
# merege_regi/merge_regi_nishi.py
#
# https://github.com/coriolis/hivex
#
# hive format doc
# https://github.com/williballenthin/python-registry/blob/master/documentation/TheWindowsNTRegistryFileFormat.pdf
#
# 1. change the following variables accroding to your env.
#    path='xp_system.new'    # hiv file path
#    reg_file="linux.reg"    # mergeide.reg  file path  use '/' letter in key
#    prefix = 'HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/'     # use '/' letter. don't use back slash
#
# 2. how to run
# $ python3 merge_regi_nishi.py
#
import sys
#import tempfile
import hivex

import re

# https://docs.python.org/ja/3/library/struct.html
# https://magazine.techacademy.jp/magazine/19058
# https://www.rox-note.tech/?p=130
import struct
import binascii

# https://zenn.dev/ynakashi/articles/15b2b7c0a3cd89

# Constants
RegSZ = 0x0001
RegExpandSZ = 0x0002
RegBin = 0x0003
RegDWord = 0x0004
RegMultiSZ = 0x0007
RegQWord = 0x000B
RegNone = 0x0000
RegBigEndian = 0x0005
RegLink = 0x0006
RegResourceList = 0x0008
RegFullResourceDescriptor = 0x0009
RegResourceRequirementsList = 0x000A
RegFileTime = 0x0010
# Following are new types from settings.dat
RegUint8 = 0x101
RegInt16 = 0x102
RegUint16 = 0x103
RegInt32 = 0x104
RegUint32 = 0x105
RegInt64 = 0x106
RegUint64 = 0x107
RegFloat = 0x108
RegDouble = 0x109
RegUnicodeChar = 0x10A
RegBoolean = 0x10B
RegUnicodeString = 0x10C
RegCompositeValue = 0x10D
RegDateTimeOffset = 0x10E
RegTimeSpan = 0x10F
RegGUID = 0x110
RegUnk111 = 0x111
RegUnk112 = 0x112
RegUnk113 = 0x113
RegBytesArray = 0x114
RegInt16Array = 0x115
RegUint16Array = 0x116
RegInt32Array = 0x117
RegUInt32Array = 0x118
RegInt64Array = 0x119
RegUInt64Array = 0x11A
RegFloatArray = 0x11B
RegDoubleArray = 0x11C
RegUnicodeCharArray = 0x11D
RegBooleanArray = 0x11E
RegUnicodeStringArray = 0x11F


class Parse:
    def __init__(self):
        self.id=0

    def encode(self,value):
        v_type = -1
        v_data = ''
        if len(value) > 7:
            if value[:6] == 'dword:':
                v_type=RegDWord
                #d_str=value[6:]
                #print('d_str=',d_str)

                i_val=int(value[6:])

                v_data = struct.pack("<i", i_val)
                #print('v_data=',v_data)


        if v_type == -1 and len(value) > 8:
            if value[:7] == 'hex(2):':
                # https://techblg.app/articles/how-to-convert-hex-to-string-python3/
                # https://stackoverflow.com/questions/5649407/hexadecimal-string-to-byte-array-in-python
                v_type = RegExpandSZ
                hex_str=value[7:]
                hex_str=re.sub(",", "", hex_str)

                #>バイト文字列 b'python3\xe3\x81\xa7string\xe3\x82\x92hex\xe5\
                hex_str=bytes.fromhex(hex_str)  # hexadecimal string to byte array in python

                #print('>hex_str=',hex_str)
                v_data=hex_str

        if v_type == -1:
            v_type=RegSZ

            #v_data = bytes(value, 'utf-8')
            dx=bytes(value, 'utf-8')

            #v_data = struct.pack('<3h', dx[0],dx[1],dx[2])
            f= str("<%dh") % (len(dx))
            v_data = struct.pack(f, *dx)

        return v_type,v_data

    def data_type_str(self,data_type):
        """
        Get the value data's type as a string
        """
        #data_type = self.data_type()
        if data_type == RegSZ:
            return "RegSZ"
        elif data_type == RegExpandSZ:
            return "RegExpandSZ"
        elif data_type == RegBin:
            return "RegBin"
        elif data_type == RegDWord:
            return "RegDWord"
        elif data_type == RegMultiSZ:
            return "RegMultiSZ"
        elif data_type == RegQWord:
            return "RegQWord"
        elif data_type == RegNone:
            return "RegNone"
        elif data_type == RegBigEndian:
            return "RegBigEndian"
        elif data_type == RegLink:
            return "RegLink"
        elif data_type == RegResourceList:
            return "RegResourceList"
        elif data_type == RegFullResourceDescriptor:
            return "RegFullResourceDescriptor"
        elif data_type == RegResourceRequirementsList:
            return "RegResourceRequirementsList"
        elif data_type == RegFileTime:
            return "RegFileTime"
        elif data_type == RegUint8:
            return "RegUint8"
        elif data_type == RegInt16:
            return "RegInt16"
        elif data_type == RegUint16:
            return "RegUint16"
        elif data_type == RegInt32:
            return "RegInt32"
        elif data_type == RegUint32:
            return "RegUint32"
        elif data_type == RegInt64:
            return "RegInt64"
        elif data_type == RegUint64:
            return "RegUint64"
        elif data_type == RegFloat:
            return "RegFloat"
        elif data_type == RegDouble:
            return "RegDouble"
        elif data_type == RegUnicodeChar:
            return "RegUnicodeChar"
        elif data_type == RegBoolean:
            return "RegBoolean"
        elif data_type == RegUnicodeString:
            return "RegUnicodeString"
        elif data_type == RegCompositeValue:
            return "RegCompositeValue"
        elif data_type == RegDateTimeOffset:
            return "RegDateTimeOffset"
        elif data_type == RegTimeSpan:
            return "RegTimeSpan"
        elif data_type == RegGUID:
            return "RegGUID"
        elif data_type == RegUnk111:
            return "RegUnk111"
        elif data_type == RegUnk112:
            return "RegUnk112"
        elif data_type == RegUnk113:
            return "RegUnk113"
        elif data_type == RegBytesArray:
            return "RegBytesArray"
        elif data_type == RegInt16Array:
            return "RegInt16Array"
        elif data_type == RegUint16Array:
            return "RegUint16Array"
        elif data_type == RegInt32Array:
            return "RegInt32Array"
        elif data_type == RegUInt32Array:
            return "RegUInt32Array"
        elif data_type == RegInt64Array:
            return "RegInt64Array"
        elif data_type == RegUInt64Array:
            return "RegUInt64Array"
        elif data_type == RegFloatArray:
            return "RegFloatArray"
        elif data_type == RegDoubleArray:
            return "RegDoubleArray"
        elif data_type == RegUnicodeCharArray:
            return "RegUnicodeCharArray"
        elif data_type == RegBooleanArray:
            return "RegBooleanArray"
        elif data_type == RegUnicodeStringArray:
            return "RegUnicodeStringArray"
        else:
            return "Unknown type: %s" % (hex(data_type))

class MergeRegi:

    def __init__(self, path,reg_file,prefix):
        self.path=path
        self.reg_file=reg_file
        self.prefix=prefix

        self.ps= Parse()

        #self.merge()

    #---------------
    # read in mergeide.reg
    #---------------
    def get_reg_file(self,path,p_sw=False):

        reg_list={}

        f = open(path)
        line = f.readline()
        sw=0
        while line:
            #print(line)
            line= line.rstrip()  
            if sw==0:
                if line.startswith('['):
                    line=re.sub("\[", "", line)
                    line=re.sub("\]", "", line)
                    line=re.sub(self.prefix, "", line)
                    key=line
                    if p_sw == True:
                        print(key)
                    val=''
                    reg_val=[]
                    sw=1
            else:       
                if len(line) == 0:
                    sw=0
                elif sw==2:
                    line=re.sub(" ", "", line)
                    if line.endswith(' '):
                        line= line[:-1]
                    #if line.endswith("\\"):
                    if line and line[-1] == '\\':
                        sw=2
                        line= line[:-1]
                    else:
                        sw=1
                    val = val + line
                    if sw == 1:
                        if p_sw == True:
                            print(val)
                        reg_val.append(val)
                        reg_list[key]=reg_val
                        val=''
                else:
                    if line and line[-1] == '\\':
                        sw=2
                        line= line[:-1]
                        val=line
                    else:
                        val=line
                        if p_sw == True:
                            print(val)
                        reg_val.append(val)
                        reg_list[key]=reg_val
                        val=''
            
            line = f.readline()

        f.close()
        return reg_list

    def get_current_control_set(self,system_hive):
        # more about windows reg control sets:
        # http://support.microsoft.com/kb/100010

        # Firstly get HKLM\SYSTEM\Select so we know which
        # ControlSetNNN is in use
        h = system_hive
        h_root = h.root()
        node = h.node_get_child(h_root, "Select")
        val = h.node_get_value(node, "Current")
        cset = "ControlSet%03d" % h.value_dword(val)
        return cset

    #---------------------------
    # print_val
    #---------------------------
    def print_val(self,n_val):
        #print("n_cur",n_cur)
        #print(n_cur_name)
        #print("n_val",n_val)
        for x in n_val:
            # python-registry/Registry/RegistryParse.py
            #print(x)
            #print(h.node_values(x))
            # 1: String
            # 2: hex(2):
            # 4: dword:
            v_type=self.h.value_type(x)
            #print('  value_type:',self.h.value_type(x))
            vx_type=self.ps.data_type_str(v_type[0])
            #print('  >vx_type='+vx_type)
            key_x=self.h.value_key(x)
            #print('key_x:',key_x)
            if v_type[0] == 1:
                val_x=self.h.value_string(x)
            elif v_type[0] == 4:
                val_x=self.h.value_dword(x)
            else:
                val_x=self.h.value_string(x)

            if v_type[0] == RegSZ:
                print('  "'+key_x+'"="'+val_x+'"')
            elif v_type[0] == RegExpandSZ:
                print('  "'+key_x+'"=hex(2):"'+val_x+'"')
            elif v_type[0] == RegDWord:
                #format(s, '*^10')
                print('  "'+key_x+'"=dword:'+format(val_x, '#08d'))
            else:
                #print('  '+key_x,'=',val_x)
                print('  "'+key_x+'"='+vx_type+':',val_x)
    
    #---------------------------
    # search_node()
    #--------------------------
    def serach_node(self,n_cset,node_list,alloc=False):
        # search node from cset=ControlSet001
        n_cur=n_cset
        for nd in node_list:
            #print('  nd:',nd)
            n_next=self.h.node_get_child(n_cur,nd)
            if n_next == None:
                if alloc==False:
                    return False,0
                else:
                    self.h.node_add_child(n_cur, nd)
                    n_next = self.h.node_get_child(n_cur, nd)
                    assert n_next,'alloc node error'

            n_cur=n_next

        return True,n_cur

    #---------------------------
    # check_stat_position()
    #--------------------------
    def check_stat_position(self):
        #print(h)
        #dir(h)
        # hive
        # $$$PROTO.HIV\ControlSet001\Control
        #
        # linux.reg
        # [HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/Control/

        h_root = self.h.root()
        h_root_name=self.h.node_name(h_root)     # h_root_name:$$$PROTO.HIV
        #print("h_root_name:",h_root_name)

        cset_name=self.get_current_control_set(self.h)    # cset=ControlSet001
        #print("cset_name=",cset_name)

        #print(h.node_get_child(h_root,cset))
        n_cset=self.h.node_get_child(h_root,cset_name)

        print('hive '+h_root_name+'\\'+cset_name)

        cset_child=self.h.node_children(n_cset)        # list []
        #print('0. ----",cset_name,'---- chiled') 
        for s in cset_child:
            n=self.h.node_name(s)
            if n in ['Control','Services']:
                print('  \\'+n)

        print('  --- Control --- chiled')
        # [HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/Control
        n_control=self.h.node_get_child(n_cset,'Control')
        n_control_child=self.h.node_children (n_control)        # list []
        for s in n_control_child:
            n=self.h.node_name(s)
            if n in ['CriticalDeviceDatabase']:
                print('    \\'+n)

        print('  --- Services --- chiled')
        n_services=self.h.node_get_child(n_cset,'Services')
        n_services_child=self.h.node_children (n_services)        # list []
        for s in n_services_child:
            n=self.h.node_name(s)
            if n in ['atapi','IntelIde','PCIIde']:
                print('    \\'+n)
        return n_cset

    #------------------------------
    # merge
    #------------------------------
    def merge(self):
        #-------------------------
        # read in mergeide.reg
        #-------------------------
        self.reg_list=self.get_reg_file(self.reg_file)

        if False:
            print("-------")
            for key in self.reg_list.keys():
                print(key)
                val = self.reg_list[key]
                for dt in val:
                    print(dt)

        # open hive with write mode
        self.h = hivex.Hivex(self.path,write = True)

        # get start node
        n_cset=self.check_stat_position()

        #--------------------------------
        # merege proc start
        #--------------------------------
        for key in self.reg_list.keys():
            #print('key:'+key)
            node_list = key.split('/')

            # search node from cset=ControlSet001
            rc,n_cur=self.serach_node(n_cset,node_list,alloc=True)
            assert rc,'alloc node error'

            n_cur_name=self.h.node_name(n_cur)     # current node name
            print("\nappend:"+self.prefix+key)      # append
            n_val = self.reg_list[key]
            n_val_list=[]
            for v in n_val:
                print('  '+v)
                (key_word,value_x) = v.split('=')

                key_word=re.sub('\"', "", key_word)
                value_x=re.sub('\"', "", value_x)
                #print('key_word='+key_word)
                #print('value_x='+value_x)

                type_x,data_x=self.ps.encode(value_x)
                #print("key:",key_word," t:",type_x," value:",data_x)

                # { "key": "Key1", "t": 3, "value": "ABC" }
                n_val_list.append({"key":key_word,"t":type_x,"value":data_x})

                #print(key_word,value_x)
                #self.set_node_value(n_cur,v)
            # https://github.com/digitalocean/hivex/blob/do/trusty/ChangeLog
            # 325 	rather than spitting out "no 'key' element in dictionary".
            #
            self.h.node_set_values(n_cur,n_val_list)

            # test
            print('--- fetch -----')
            n_val=self.h.node_values(n_cur)
            self.print_val(n_val)

            #print(h.node_get_value(n_cur,"ClassGUID"))
            #print(h.node_get_value(n_cur,"Service"))

            #return
        
        # commit hiv file
        self.h.commit(self.path)
        # close hiv
        del self.h

    #------------------------------
    # compare check
    #------------------------------
    def comp_check(self):
        #-------------------------
        # read in mergeide.reg
        #-------------------------
        self.reg_list=self.get_reg_file(self.reg_file)

        if False:
            print("-------")
            for key in self.reg_list.keys():
                print(key)
                val = self.reg_list[key]
                for dt in val:
                    print(dt)

        # open hive with write mode
        self.h = hivex.Hivex(self.path)

        # get start node
        n_cset=self.check_stat_position()

        #--------------------------------
        # compare proc start
        #--------------------------------
        for key in self.reg_list.keys():
            #print('key:'+key)
            node_list = key.split('/')

            print("\ncheck:"+self.prefix+key)
            n_val = self.reg_list[key]
            n_val_list=[]
            for v in n_val:
                print('  '+v)
                (key_word,value_x) = v.split('=')

                key_word=re.sub('\"', "", key_word)
                value_x=re.sub('\"', "", value_x)
                #type_x,data_x=self.ps.encode(value_x)
                
                #n_val_dic={}
                #n_val_dic[key_word]=value_x

                #print("key:",key_word," t:",type_x," value:",data_x)

                # { "key": "Key1", "t": 3, "value": "ABC" }
                #n_val_list.append({"key":key_word,"t":type_x,"value":data_x})
                #print(key_word,value_x)
                #self.set_node_value(n_cur,v)

            # search node from cset=ControlSet001
            rc,n_cur=self.serach_node(n_cset,node_list,alloc=False)
            #assert rc,'search node failed'
            if rc == False:
                print('--- nothing -----')
                continue

            #n_cur_name=self.h.node_name(n_cur)     # current node name

            # https://github.com/digitalocean/hivex/blob/do/trusty/ChangeLog
            # 325 	rather than spitting out "no 'key' element in dictionary".
            #
            #h.node_set_values(n_cur,n_val_list)
            # test
            print('--- fetch -----')
            n_val=self.h.node_values(n_cur)
            self.print_val(n_val)
            #print(h.node_get_value(n_cur,"ClassGUID"))
            #print(h.node_get_value(n_cur,"Service"))
        
        # close hiv
        del self.h

if __name__ == "__main__":

    # ---- hiv file path definition ----
    path='xp_system.new' 
    #path='xp_system.org'

    # ---- mergeide.reg file path, use '/' letter. don't use back slash in key fields ---
    #                                       in data fields, back slash ok
    reg_file="linux.reg" 
    #reg_file="linux_test.reg"

    # ---- prefix letters definition ----
    prefix = 'HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/'     # use '/' letter. don't use back slash

    #reg_file='MergeIDE.reg'
    #prefix = 'HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/'

    mrg=MergeRegi(path,reg_file,prefix)

    # exec merge
    mrg.merge()
    # exec check
    #mrg.comp_check()