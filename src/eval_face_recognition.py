import io

import torch
import torchvision.transforms as transforms
from PIL import Image
import json
import numpy as np
import build_custom_model

def recognize_face(image):
     labels_dir = "./checkpoint/labels.json"
     model_path = "./checkpoint/model_vggface2_best.pth"


     # read labels
     with open(labels_dir) as f:
          labels = json.load(f)
     print(f"labels: {labels}")


     device = torch.device('cpu')
     model = build_custom_model.build_model(len(labels)).to(device)
     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
     model.eval()
     print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")


     img = Image.open(io.BytesIO(image))
     img_tensor = transforms.ToTensor()(img).unsqueeze_(0).to(device)
     outputs = model(img_tensor)
     _, predicted = torch.max(outputs.data, 1)
     result = labels[np.array(predicted.cpu())[0]]
     # print(predicted.data, result)


     print(f"Image recognition result is: {result}")
     return result

if __name__ == "__main__":
     with open('data/test_me/val/Krishna/image_2022-05-06_22.42.27.png', 'rb') as test_image_file:
          test_image = test_image_file.read()
          recognize_face(test_image)