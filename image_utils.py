import fitz
import os

def extract_images(pdf_path, output_dir="images"):

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    image_paths = []

    for i in range(len(doc)):
        page = doc[i]
        images = page.get_images(full=True)

        for j, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            path = f"{output_dir}/img_{i}_{j}.png"
            pix.save(path)
            image_paths.append(path)

    return image_paths