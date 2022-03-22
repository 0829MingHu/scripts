"""
移动视频
"""
import cv2 
import os 
import re


source_dir='./result'
target_dir_less10='./less10'
target_dir_more10='./more10'
os.makedirs(target_dir_less10,exist_ok=True)
os.makedirs(target_dir_more10,exist_ok=True)


class VideoMover:

    def get_files(self,dir):
        """
        获取所有的MP4文件
        """
        all_files=[]
        for root,dirs,files in os.walk(dir):
            for file in files:
                if file.endswith('.mp4'):
                    all_files.append(os.path.join(root,file).replace('\\','/'))
        return all_files


    def get_video_duration(self,filename):
        cap = cv2.VideoCapture(filename)
        if cap.isOpened():
            rate = cap.get(5)
            frame_num =cap.get(7)
            duration = round(frame_num/rate,0)
            return duration
        return -1

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


    def move_all_format_file(self,mp4_file):
        """
        根据视频路径，移动相同路径下的mp4、vtt、m4a文件
        Z_cDpE1xvI4
        """
        #正则匹配YouTube视频ID
        id=re.findall('[a-zA-Z0-9_-]{11}',mp4_file)[0]
        # id='xxxxx'
        #获取视频目录路径
        dir_path=os.path.dirname(mp4_file)
        #提取动作列表
        action_path=self.extract_action_path(mp4_file)
        #目标路径
        duration=self.get_video_duration(mp4_file)
        if duration<=10*60:
            target_dir=target_dir_less10
        else:
            target_dir=target_dir_more10
        target_dir=os.path.join(target_dir,action_path)
        #创建目标路径
        os.makedirs(target_dir,exist_ok=True)
        #目标文件
        target_file=os.path.join(target_dir,os.path.basename(mp4_file))
        #当前目录下同ID的vtt、m4a文件
        vtt_file,target_vtt_file='',''
        m4a_file,target_m4a_file='',''
        files=os.listdir(dir_path)
        for file in files:
            if id in file:
                if 'vtt' in file:
                    vtt_file=os.path.join(dir_path,file)
                    target_vtt_file=os.path.join(target_dir,os.path.basename(file))
                elif 'm4a' in file:
                    m4a_file=os.path.join(dir_path,file)
                    target_m4a_file=os.path.join(target_dir,os.path.basename(file))
        # print(os.path.join(dir_path,vtt_file),os.path.join(dir_path,m4a_file))
        # # 移动mp4、vtt、m4a文件
        if vtt_file:
            print(f'{vtt_file}-->{target_vtt_file}')
            os.rename(vtt_file,target_vtt_file)
        if m4a_file:
            print(f'{m4a_file}-->{target_m4a_file}')
            os.rename(m4a_file,target_m4a_file)
        print(f'{mp4_file}-->{target_file}')
        os.rename(mp4_file,target_file)
        print(f'{mp4_file}及其相关文件移动成功')


    def main(self):
        all_files=self.get_files(source_dir)
        for file in all_files:
            self.move_all_format_file(file)


if __name__=='__main__':
    vm=VideoMover()
    vm.main()