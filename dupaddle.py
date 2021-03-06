from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import cv2


OCR_DEBUG = True


def ocrProcess(img):
    global OCR_DEBUG
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', det_limit_side_len=1920,
                    det_model_dir=r"D:\Program\Project\ncnn-master\paddle_ocr\ch_ppocr_server_v2.0_det_infer",
                    rec_model_dir=r"D:\Program\Project\ncnn-master\paddle_ocr\ch_ppocr_server_v2.0_rec_infer") # need to run only once to download and load model into memory

    result = ocr.ocr(img, cls=True)

    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]

    if OCR_DEBUG:
        image = Image.fromarray(img).convert('RGB')

        for line in result:
            print(line)

        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save(r'D:\Dataset\ocr/result.jpg')

        img2 = img.copy()
        for box in boxes:
            cv2.rectangle(img2, (int(box[0][0]), int(box[0][1])), (int(box[2][0]), int(box[2][1])), (0, 255, 0), 15)
        cv2.imwrite(r'D:\Dataset\ocr/result.png', img2)
    return boxes, txts


if __name__ == "__main__":
    img = cv2.imread(r"D:\Dataset\ocr\0003.jpg")
    boxes, txts = ocrProcess(img)
    print(txts)
    print(boxes)
    print(len(txts))
    print(len(boxes))