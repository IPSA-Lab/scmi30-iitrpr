from __future__ import print_function
from __future__ import print_function
from __future__ import division
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import torchvision
import matplotlib.pyplot as plt
import csv
from torchvision import models
import time
import cv2
import os
import glob
from pathlib import Path
import os
import copy
# print("PyTorch Version: ",torch.__version__)
# print("Torchvision Version: ",torchvision.__version__)
import scipy.io
import numpy as np
from pathlib import Path
import torch.utils.data as data
import pandas as pd
import torch.utils.data as data

from PIL import Image
import os
import os.path

IMG_EXTENSIONS = [
   '.jpg', '.JPG', '.jpeg', '.JPEG',
   '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP','.mat',
]


def is_image_file(filename):
   return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)

def find_classes(dir):
   classes = os.listdir(dir)
   classes.sort()
   class_to_idx = {classes[i]: i for i in range(len(classes))}
   return classes, class_to_idx


def make_dataset(dir, class_to_idx):
   images = []
   for target in os.listdir(dir):
       d = os.path.join(dir, target)
       if not os.path.isdir(d):
           continue

       for filename in os.listdir(d):
           if is_image_file(filename):
               path = '{0}/{1}'.format(target, filename)
               #print(path)
               item = (path, class_to_idx[target])
               images.append(item)

   return images

def default_loader(path):
   return Image.open(path).convert('RGB')

def mat_loader(path):
   return scipy.io.loadmat(path1)

class ImageFolderLoader(data.Dataset):
   def __init__(self, root1,transform_1=None,
                target_transform=None,
                loader=default_loader):
       classes1, class_to_idx1 = find_classes(root1)
       
       imgs1 = make_dataset(root1, class_to_idx1)
      

       self.root1 = root1
       self.imgs1 = imgs1
       self.classes1 = classes1
       self.class_to_idx1 = class_to_idx1
       self.target_transform = target_transform
       self.loader = loader
       self.img_transform = transform_1
        
       
       

   def __getitem__(self, index):
    

       path1, target1 = self.imgs1[index]
       filename = Path(path1).stem 
    
       img1 = self.loader(os.path.join(self.root1, path1))  
       
       if self.img_transform is not None:
           img1 = self.img_transform(img1)
        
       img1 = np.array(img1) 
       img1 = torch.from_numpy((img1)).float() 

        
       if self.target_transform is not None:
           target1 = self.target_transform(target)
        
       target1 = torch.eye(30)[target1]      
            
       #print(img1.shape,img_mat.shape)      

       return img1,target1,filename

   def __len__(self):
       return len(self.imgs1)
    

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
        self.rem1_conv1 = nn.Conv2d(in_channels=3,out_channels=64,kernel_size=(3,3),stride=1,padding=1)
        self.rem1_bn1 = nn.BatchNorm2d(64)
        self.rem1_conv2 = nn.Conv2d(in_channels=67,out_channels=64,kernel_size=(3,3),stride=1,padding=1)
        self.rem1_bn2 = nn.BatchNorm2d(64)
        self.rem1_conv3 = nn.Conv2d(in_channels=67,out_channels=3,kernel_size=(3,3),stride=1,padding=1)
        self.rem1_bn3 = nn.BatchNorm2d(3)
        
        
        self.rem2_conv1 = nn.Conv2d(in_channels=3,out_channels=128,kernel_size=(3,3),stride=1,padding=1)
        self.rem2_bn1 = nn.BatchNorm2d(128)
        self.rem2_conv2 = nn.Conv2d(in_channels=131,out_channels=128,kernel_size=(3,3),stride=1,padding=1)
        self.rem2_bn2 = nn.BatchNorm2d(128)
        self.rem2_conv3 = nn.Conv2d(in_channels=131,out_channels=3,kernel_size=(3,3),stride=1,padding=1)
        self.rem2_bn3 = nn.BatchNorm2d(3)
        
        self.rem3_conv1 = nn.Conv2d(in_channels=3,out_channels=256,kernel_size=(3,3),stride=1,padding=1)
        self.rem3_bn1 = nn.BatchNorm2d(256)
        self.rem3_conv2 = nn.Conv2d(in_channels=259,out_channels=256,kernel_size=(3,3),stride=1,padding=1)
        self.rem3_bn2 = nn.BatchNorm2d(256)
        self.rem3_conv3 = nn.Conv2d(in_channels=259,out_channels=3,kernel_size=(3,3),stride=1,padding=1)
        self.rem3_bn3 = nn.BatchNorm2d(3)
        
        
        self.conv1 = nn.Conv2d(in_channels=3,out_channels=64,kernel_size=(7,7),stride=2)
        self.bn1 = nn.BatchNorm2d(64)
        self.prelu1 = nn.PReLU()
        
        self.conv2 = nn.Conv2d(in_channels=64,out_channels=128,kernel_size=(5,5),stride=2)
        self.bn2 = nn.BatchNorm2d(128)
        self.prelu2 = nn.PReLU()
        
        self.conv3 = nn.Conv2d(in_channels=128,out_channels=256,kernel_size=(3,3),stride=2)
        self.bn3 = nn.BatchNorm2d(256)
        self.prelu3 = nn.PReLU()
        
        self.conv4 = nn.Conv2d(in_channels=256,out_channels=512,kernel_size=(2,2),stride=2,padding=1)
        self.bn4 = nn.BatchNorm2d(512)
        self.prelu4 = nn.PReLU()
        
   
        self.avgpool1= nn.AvgPool2d(kernel_size=(4,4),stride=2)
        
        self.conv5 = nn.Conv2d(in_channels=512,out_channels=30,kernel_size=(1,1),stride=1)
        
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x1):
        
        x = x1
        x = self.rem1_conv1(x)
        x = self.rem1_bn1(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem1_conv2(x)
        x = self.rem1_bn2(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem1_conv3(x)
        x = self.rem1_bn3(x)
        
        x = x1-x
        x1= x
        
    
        x = self.rem2_conv1(x)
        x = self.rem2_bn1(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem2_conv2(x)
        x = self.rem2_bn2(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem2_conv3(x)
        x = self.rem2_bn3(x)
        
        x = x1-x
        x1= x
        
        
        x = self.rem3_conv1(x)
        x = self.rem3_bn1(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem3_conv2(x)
        x = self.rem3_bn2(x)
        x = torch.cat((x,x1),dim=1)
        x = self.rem3_conv3(x)
        x = self.rem3_bn3(x)
        
        x = x1 - x
        
        
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.prelu1(x)
        
        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.prelu2(x)
        
        
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.prelu3(x)
        
        
        x = self.conv4(x)
        x = self.bn4(x)
        x = self.prelu4(x)
        
        x = self.avgpool1(x)
        
        x = self.conv5(x)
        
        x = x.view(x.size(0), -1)
        
        x = self.softmax(x)
       
        return x
    
def custom_categorical_cross_entropy(y_pred, y_true):
    y_pred = torch.clamp(y_pred, 1e-32, 1 - 1e-32)
    return -(y_true * torch.log(y_pred)).sum(dim=1).mean()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Your program description')
    parser.add_argument('--data', required=True, help='Data directory path')
    parser.add_argument('--model', required=True, help='Model path')
    args = parser.parse_args()

    data_dir = args.data
    model_path = args.model

    print("PyTorch Version: ", torch.__version__)
    print("Torchvision Version: ", torchvision.__version__)

    data_transforms = transforms.Compose([
      transforms.ToTensor()
    ])
    
    classes1, class_to_idx1 = find_classes(data_dir)
    imgs1 = make_dataset(data_dir, class_to_idx1)
    print(class_to_idx1,len(imgs1))
       
    imgs1 = make_dataset(data_dir, class_to_idx1)

    batchsize = 1

    val_dataset = ImageFolderLoader(
        data_dir,
        data_transforms
    )

    test_loader = torch.utils.data.DataLoader(
        val_dataset, batch_size=batchsize,
        shuffle=False, num_workers=4
    )

    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda:0')
    # print(device)
    model = Net().to(device)
    model = torch.load(model_path)
    model.eval()

    results_folder = "Results_Rafi"
    if os.path.exists(results_folder):
        # If it exists, delete the folder and its content
        print("Deleting existing Results_Rafi folder...")
        for file in os.listdir(results_folder):
            file_path = os.path.join(results_folder, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    a = -1
    os.makedirs(results_folder, exist_ok=True)

    with torch.no_grad():
        for batch_idx, (imgs1, labels1,patch_filename) in enumerate(test_loader):
            _, c = torch.max(labels1.data,1)
            d = c.cpu().numpy()[0]

            if(d!=a):
                print("Yes_Class",d)
                a= d
                z = d
                file_class = os.path.join(results_folder, f"Test_Class_{z}.csv")


                with open(file_class, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Batch_Id","Patch_Filename","True Class","Predicted Class","Probability of Predicted Class"])



            img_org,target = imgs1.to(device,dtype=torch.float), labels1.to(device)
            #img_org = img_org.permute(0, 3, 1, 2)

            output = model(img_org)


            _, actual = torch.max(target.data, 1)    
            _, predicted = torch.max(output.data, 1)

            y_true = actual.cpu().numpy()[0]
            y_pred =predicted.cpu().numpy()[0]

            prob_y_pred = output[0][y_pred]
            prob_y_pred = prob_y_pred.cpu().numpy()
            prob_y_pred = np.around(prob_y_pred,decimals=2)

            if(batch_idx % 1000 == 0):
              print(batch_idx,patch_filename,y_true,y_pred,prob_y_pred)


            with open(file_class, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([batch_idx,patch_filename,y_true,y_pred,prob_y_pred])



    csv_dir = img_dir = "Results_Rafi/"
    data_path = os.path.join(img_dir,'*csv')
    files = glob.glob(data_path)
    
    results_folder = "Results_Rafi_Clusters"
    if os.path.exists(results_folder):
        # If it exists, delete the folder and its content
        print("Deleting existing Results_Rafi_Clusters folder...")
        for file in os.listdir(results_folder):
            file_path = os.path.join(results_folder, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    os.makedirs(results_folder, exist_ok=True)
    
    a = "a"
    
    for f in files:
        print(f)
        b = "-1"
        d = Path(f).stem
        classname = Path(f).stem
        classname = int(classname.split("_")[2])

        true_image_class = classname

        if(d!=a):
            a = d
            file_class = os.path.join(results_folder, f"Test_Class_{a}.csv")
            with open(file_class, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Batch_Id","Cluster_Name","True Class","Predicted Class","Probability of Predicted Class"])


        df = pd.read_csv(f)
        data = df.sort_values(by=['Patch_Filename'])
        data = data.to_numpy()

        predictions = []

        for i in range(len(data)):

            patchname = data[i][1]
            clustername =patchname.split("_")[:-1]
            clustername = "_".join(clustername)

            if(b!=clustername and b!="-1"):
                b = clustername

                pred_img_label  = max(predictions,key=predictions.count)
                prob = (predictions.count(pred_img_label))/len(predictions)
                pred_img_label = int(pred_img_label)


                with open(file_class, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([i, clustername ,true_image_class,pred_img_label,prob])

                predictions = []
                predicted_label = data[i][3]
                predictions.append(predicted_label)

            elif(b!=clustername and b =="-1"):
                b = clustername

                predictions = []
                predicted_label = data[i][3]
                print(predicted_label)
                predictions.append(predicted_label)

            elif(b==clustername):
                predicted_label = data[i][3]
                predictions.append(predicted_label)
            else:
                print("Done")


        pred_img_label  = max(predictions,key=predictions.count)
        prob = (predictions.count(pred_img_label))/len(predictions)
        pred_img_label = int(pred_img_label)


        with open(file_class, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i, clustername ,true_image_class,pred_img_label,prob])

        predictions = []

    csv_dir = img_dir = "Results_Rafi_Clusters/"
    data_path = os.path.join(img_dir,'*csv')
    files = glob.glob(data_path)

    with open(os.path.join(csv_dir + 'Image_Level_Results.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image Class Label","Number of Images",\
                         "Correct Predicted Images",\
                         "Number of Patches",\
                         "Total Patches(Correct Classified Images)",\
                         "Correct Predicted Patches(Correct Classified Images)",\
                         "Precetange Votes Per Image(Only Correct Images)",\
                         "Average Softmax Probability of Correct Patch(Only Correct Images)"])
        
    for f in files:
        df = pd.read_csv(f)
        data = df.sort_values(by=['Cluster_Name'])
        classname = Path(f).stem
        classname = int(classname.split("_")[-1])
        a="a"

        true_image_class = classname
        total_images_perclass = 0
        correct_images_perclass = 0
        total_patches_perclass = 0

        total_class_votes =0
        total_class_patches =0
        prob_avg_correct_patch = 0.0
        votes = 0

        arr_pred_patches = []
        arr_pred_patches_prob = []
        total_correc_img_patches = 0


        for ind in data.index:
                filename = df['Cluster_Name'][ind]
                pred_patch_class = df['Predicted Class'][ind]
                pred_patch_prob = df['Probability of Predicted Class'][ind]

                filename = filename.split("_")
                file_length = len(filename)
                initial_filename = filename[:-1]
                patch_name = filename[file_length-1]
                #print(initial_filename)
                #print(patch_name)

                if(a!= initial_filename and a=="a"):
                    a = initial_filename



                if(a!=initial_filename and a!="a"):
                    total_images_perclass = total_images_perclass + 1

                    counts = np.bincount(arr_pred_patches)
                    pred_image_class = np.argmax(counts)
                    votes = np.count_nonzero(arr_pred_patches==pred_image_class)
                    s=0

                    if(pred_image_class == true_image_class):
                        correct_images_perclass = correct_images_perclass + 1
                        total_class_votes = total_class_votes + votes
                        total_class_patches = total_class_patches + len(arr_pred_patches)

                        total_correc_img_patches = total_correc_img_patches + len(arr_pred_patches)

                        z = np.where(np.array(arr_pred_patches)==true_image_class,1,0)
                        for i in range(0,len(arr_pred_patches)):
                            if(z[i]==1):
                                s= s+1
                                prob_avg_correct_patch = prob_avg_correct_patch + arr_pred_patches_prob[i]

                    arr_pred_patches = []
                    arr_pred_patches_prob = []
                    a = initial_filename



                if(a==initial_filename):
                    total_patches_perclass = total_patches_perclass + 1
                    arr_pred_patches.append(pred_patch_class)
                    arr_pred_patches_prob.append(pred_patch_prob)



        total_images_perclass = total_images_perclass + 1

        counts = np.bincount(arr_pred_patches)
        pred_image_class = np.argmax(counts)
        votes = np.count_nonzero(arr_pred_patches==pred_image_class)

        if(pred_image_class == true_image_class):
            correct_images_perclass = correct_images_perclass + 1
            total_class_votes = total_class_votes + votes
            total_class_patches = total_class_patches + len(arr_pred_patches)

            total_correc_img_patches = total_correc_img_patches + len(arr_pred_patches)

            z = np.where(np.array(arr_pred_patches)==true_image_class,1,0)
            for i in range(0,len(arr_pred_patches)):
                if(z[i]==1):
                    prob_avg_correct_patch = prob_avg_correct_patch + arr_pred_patches_prob[i]

        arr_pred_patches = []
        arr_pred_patches_prob = []

        if(correct_images_perclass!=0):
            prob_avg_correct_patch = prob_avg_correct_patch / total_class_votes
            prob_avg_correct_patch = np.around(prob_avg_correct_patch,decimals=2)
            avg_vote_perclass = np.around((total_class_votes*100) / total_correc_img_patches,decimals=2)
            print(total_images_perclass,total_patches_perclass,correct_images_perclass,total_class_votes,avg_vote_perclass,prob_avg_correct_patch)  

            with open(os.path.join(csv_dir + 'Image_Level_Results.csv'), 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([classname,total_images_perclass,correct_images_perclass,total_patches_perclass,\
                                 total_correc_img_patches,total_class_votes,\
                                 avg_vote_perclass,\
                                 prob_avg_correct_patch])
        else:
            with open(os.path.join(csv_dir + 'Image_Level_Results.csv'), 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([classname,total_images_perclass,correct_images_perclass,total_patches_perclass,\
                                 total_correc_img_patches,total_class_votes,\
                                 avg_vote_perclass,\
                                 prob_avg_correct_patch])

    df = pd.read_csv(os.path.join(csv_dir + 'Image_Level_Results.csv'))

    ILA = sum(df['Correct Predicted Images']) / sum(df['Number of Images']) * 100
    
    print(f"Image Level Accuracy: {ILA}%")