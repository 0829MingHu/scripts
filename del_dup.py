
import os 
import hashlib
import re

cmp_dir1=r"H:\测试\path1" ##这个目录下的重复文件会被删除
cmp_dir2=r"H:\测试\path2" ##这个目录下和上个目录对比，如果有重复文件，则这个目录的重复文件会被删除
delete=False

class DuplicateFinder:

    def get_files(self,dir):
        """
        获取所有的MP4文件
        """
        all_files=[]
        for root,dirs,files in os.walk(dir):
            for file in files:
                if file.endswith('.mp4'):
                    all_files.append(os.path.join(root,file))
        return all_files

    def chunk_reader(self, fobj, chunk_size: int = 1024):
        """
        Generator that reads a file in chunks of bytes
        """
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def get_hash(self,filename: str):
        """
        Gets the hash of either the first chunk of file or whole file.
        """
        hashobj = hashlib.sha1()
        with open(filename, "rb") as _f:
            for chunk in self.chunk_reader(_f):
                hashobj.update(chunk)
        return hashobj.digest()
    
    def delete_all_format_file(self,mp4_file):
        """
        根据视频路径，删除相同路径下的mp4、vtt、m4a文件
        Z_cDpE1xvI4
        """
        #正则匹配YouTube视频ID
        id=re.findall('[a-zA-Z0-9_-]{11}',mp4_file)[0]
        # id='xxxxx'
        #获取视频目录路径
        dir_path=os.path.dirname(mp4_file)
        #当前目录下同ID的vtt、m4a文件
        vtt_file=''
        m4a_file=''
        files=os.listdir(dir_path)
        for file in files:
            if id in file:
                if 'vtt' in file:
                    vtt_file=file
                elif 'm4a' in file:
                    m4a_file=file
        # print(os.path.join(dir_path,vtt_file),os.path.join(dir_path,m4a_file))
        # # 删除mp4、vtt、m4a文件
        if delete:
            if vtt_file:
                os.remove(os.path.join(dir_path,vtt_file))
            if m4a_file:
                os.remove(os.path.join(dir_path,m4a_file))
            os.remove(mp4_file)
            print(f'{mp4_file}及其相关文件删除成功')
        else:
            print(f'重复视频：{mp4_file}')

    def extract_action_path(self,file):
        """
        获取family/genus/keyword/action分类
        返回分类路径
        """
        #判断分隔符
        if '/' in file:
            action_path=file.split('/')[-5:-1]
        else:
            action_path=file.split('\\')[-5:-1]
        return '/'.join(action_path)


    def find_and_duplicate_files(self,dir_dict:dict):
        """
        查找相同family/genus/keyword/action下的重复文件
        输入格式：{'family/genus/keyword/action':[file1,file2]}
        """
        action,files=dir_dict.popitem()
        hash_dict={}
        for file in files:
            hash=self.get_hash(file)
            hash_dict.setdefault(hash,[]).append(file)
        
        dup_hash_dict={}
        for hash,files in hash_dict.items():
            if len(files)>1:
                print(f'action:{action}-相同hash:{hash}的重复文件数：{len(files)}')
                dup_hash_dict[hash]=files
        return dup_hash_dict

    
    def delete_files(self,files):
        """
        删除重复文件
        1. /down_videos/documentary下面的重复文件都删除
        2. /down_videos/1.15下面的重复文件，保留一个
        """
        # print(files)
        del_files=[]
        for file in files:
            # print(file)
            if cmp_dir2 in file:
                del_files.append(file)
                files.remove(file)
        #如果files文件数量大于1，则删除重复文件
        if len(files)>1:
            # print(files)
            for idx,file in enumerate(files):
                if idx==0:
                    continue
                else:
                    # print(file)
                    del_files.append(file)
        #删除重复文件
        # print('del_files:',del_files)
        for file in del_files:
            self.delete_all_format_file(file)
            # print(f'{file}删除成功')
    
    def main(self):
        print('开始查找所有视频文件')
        cmp_dir1_files=self.get_files(cmp_dir1)
        cmp_dir2_files=self.get_files(cmp_dir2)
        all_files=cmp_dir1_files+cmp_dir2_files
        action_files_dict={}
        print('抽取相同family/genus/keyword/action下的文件')
        for file in all_files:
            action=self.extract_action_path(file)
            action_files_dict.setdefault(action,[]).append(file)
        #重复文件
        print('查找相同family/genus/keyword/action下的重复文件')
        dup_files={}
        for action,files in action_files_dict.items():
            dup=self.find_and_duplicate_files({action:files})
            if dup:
                dup_files[action]=dup
        # print(dup_files)
        print('删除重复文件')
        #删除重复文件
        for action,hash_files in dup_files.items():
            for hash,files in hash_files.items():
                self.delete_files(files)
                






if __name__=='__main__':
    DuplicateFinder().main()
        