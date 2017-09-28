from lib.tf_style_transfer import save_image_sbs, load_image, save_image_sbs2
from PIL import Image

img1 = "/home/grusinator/git_ws/python/AAnder_geocatch/data/face-input.jpg"
img2 = "/home/grusinator/git_ws/python/AAnder_geocatch/data/face-input.jpg"
img3 = "/home/grusinator/git_ws/python/AAnder_geocatch/data/out.jpg"

#org_image1 = load_image(img1)
#org_image2 = load_image(img2)
#org_image3 = load_image(img3)

org_image1 = Image.open(img1)
org_image2 = Image.open(img2)
org_image3 = Image.open(img3)

print(type(org_image2))


out =  "/home/grusinator/git_ws/python/AAnder_geocatch/data/out2.jpg"

save_image_sbs2(out, org_image1,org_image2, org_image3)


