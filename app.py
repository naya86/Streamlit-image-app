import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import os     
from datetime import datetime  

##깃 연동.
def load_image(image_file) :          
    img = Image.open(image_file)
    return img


## 디렉토리와 이미지를 주면, 해당 디렉토리에 이 이미지를 저장하는함수
def save_uploaded_file(directory, img) :
    # 1.디렉토리가 있는지 확인하여, 없으면 만든다.
    if not os.path.exists(directory) :
        os.makedirs(directory)
    # 2.이제는 디렉토리가 있으니, 이미지을 저장
    filename = datetime.now().isoformat().replace(':','-').replace('.','-')
    img.save(directory+'/'+filename+'.jpg')
    return st.success('Saved file : {} in {}'.format(filename+'.jpg', directory))


def main() :
    # img = Image.open('data/birds.jpg')
    # st.image(img)           ##   (img, use_columns_width = True )
    
    # 1.파일을 업로드하는걸로 바꿔오기
    
    image_file_list = st.file_uploader('이미지 파일 업로드', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    #print(image_file_list)
    # 파일이 있을경우에만 실행되기위해 if 에 넣어줌.
    if image_file_list is not None :
        # 2 각 파일을 이미지로 바꿔줘야 한다.
        image_list = []
        for image_file in image_file_list:           #모든 파일이 image_list에 이미지로 저장됨.
            img = load_image(image_file)
            image_list.append(img)
 

        option_list = ['Show Image', 'Rotate Image', 'Create Thumbnail', 'Crop Image', 'Merge Images', 'Flip Image', 'Change Color', 'Filters - Sharpen', 
                    'Filters - Edge Enhance', 'Contrast Image']  #Thumbnail 원본이미지를 작게 만드는것.
        option = st.selectbox('옵션을 선택하세요.', option_list)

        
        if option == 'Show Image' :
            for img in image_list :
                st.image(img)
            directory = st.text_input('저장 폴더명 입력')
            if st.button('Save') :
               for img in image_list:
                save_uploaded_file(directory, img)    
        
        elif option == 'Rotate Image' :           ## 사진파일 돌리기
            #유저가 입력
            degree = st.number_input('각도입력', 0, 360 )
            #모든 이미지를 돌린다.
            trainsformed_img_list = []
            for img in image_list :
                rotate_img = img.rotate(degree)
                # img.save('data/rot.jpg')          
                st.image(rotate_img)
                trainsformed_img_list.append(rotate_img)  
            
            directory = st.text_input('저장 폴더명 입력')
            if st.button('Save') :
               for img in trainsformed_img_list:
                save_uploaded_file(directory, img)

           

        elif option == 'Create Thumbnail' :            #thumbnail 함수 이용
            ## 1. 이미지의 사이즈를 먼저 알아야한다.
            ## 가장 작은 이미지를 찾아서 그 사이즈로 한다.
            width = st.number_input('width입력', 1, 100 )
            height = st.number_input('height입력', 1, 100 )
            size = (width, height)
            
            trainsformed_img_list = []
            for img in image_list:
                img.thumbnail( size )
                st.image(img)
                trainsformed_img_list.append(img)

            # 저장은 여기서.

            directory = st.text_input('저장 폴더명 입력')
            if st.button('Save') :
               for img in trainsformed_img_list:
                save_uploaded_file(directory, img)
            

                   
        # elif option == 'Crop Image' :    #이미지를 자른다.
        #     # 왼쪽 윗부분부터 시작해서, 너비와 깊이만큼 잘라라
        #     start_x = st.number_input('시작 x좌표', 0, img.size[0]-1 )
        #     strat_y = st.number_input('시작 y좌표', 0, img.size[1]-1 )
        #     max_width = img.size[0] - start_x
        #     max_height = img.size[1] - strat_y
        #     width = st.number_input('width입력',1, max_width )
        #     height = st.number_input('width입력', 1, max_height )         ## 예외처리도 넣었다.
        #     box = (start_x, strat_y, start_x + width, strat_y + height)
        #     cropped_img = img.crop(box)
        #     cropped_img.save('data/crop.png')
        #     st.image(cropped_img)

        # elif option == 'Merge Images' :
        #     merge_file = st.file_uploader('이미지 파일 업로드', type=['png', 'jpg', 'jpeg'], key='merge')
                       
        #     if merge_file is not None :
                
        #         merge_img = load_image(merge_file)   #이미지 불러오기   (사용자가 선택한 이미지를 활용하도록 바꿔넣기)    
                
        #         start_x = st.number_input('시작 x좌표', 0, img.size[0]-1 )
        #         strat_y = st.number_input('시작 y좌표', 0, img.size[1]-1 )
                
        #         position = (start_x, strat_y )   #여기에 붙여라
        #         img.paste(merge_img, position)           ##기존 이미지 사이즈 안쪽에 들어오도록 포지션을 정해야 합쳐진다.
        #         st.image(img)

        elif option == 'Flip Image' :             ## 이미지 반전.
            status = st.radio('플립 선택', ['FLIP_TOP_BOTTOM', 'FLIP_LEFT_RIGHT'])                            
            
            if status == 'FLIP_TOP_BOTTOM' :
                trainsformed_img_list = []
                
                for img in image_list:
                    flipped_img = img.transpose( Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_img)
                    trainsformed_img_list.append(flipped_img)

            elif status ==  'FLIP_LEFT_RIGHT' :
                trainsformed_img_list = []
                
                for img in image_list :
                    flipped_img = img.transpose( Image.FLIP_LEFT_RIGHT)
                    st.image(flipped_img) 
                    trainsformed_img_list.append(flipped_img)

            directory = st.text_input('저장 폴더명 입력')
            if st.button('Save') :
                for img in trainsformed_img_list:
                    save_uploaded_file(directory, img)    

        
        # elif option == 'Change Color' :
        #     status = st.radio('색 변경', ['Color', 'Gray Scale', 'Black & White'])
            
        #     if status == 'Color' :
        #         color = 'RGB'
        #     elif status == 'Gray Scale' :
        #         color = 'L'
        #     elif status == 'Black & White':
        #         color = '1'
            
        #     bw = img.convert(color)                #1은 블랙앤화이트  #L은 흑백(그레이스케일(0~255))
        #     st.image(bw)

        # elif option == 'Filters - Sharpen' :                #선명하게
        #     sharp_img = img.filter(ImageFilter.SHARPEN)
        #     st.image(sharp_img)

        # elif option == 'Filters - Edge Enhance' :       ## 선들을 조금 더 강하게!!
        #     edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
        #     st.image(edge_img)

        # elif option == 'Contrast Image' :           ##명암 조절
        #     contrast_img = ImageEnhance.Contrast(img).enhance(2)        #  2는 enhance의 단계
        #     st.image(contrast_img)

        
    

if __name__ == '__main__' :
    main()
