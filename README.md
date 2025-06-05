# PDFDecrypter

This repository contains:

* A Python script (`remove_pdf_security.py`) that:
  * Scans all PDF files in `./data/`
  * Tries to decrypt each PDF with an empty password
  * Outputs a fully unlocked copy (with the same filename) into `./processed/`
* A `Dockerfile` that packages the script and its dependencies (`PyPDF2` and `pycryptodome`) into a container
* A simple folder structure so that you can drop your protected PDFs into `data/` and get decrypted copies in `processed/` without extra setup

---

## Table of Contents

1. [Problem](#problem)
2. [Solution](#solution)
3. [Project Structure](#project-structure)
4. [Setup & Usage](#setup--usage)

   1. [Prerequisites](#prerequisites)
   2. [Building the Docker Image](#building-the-docker-image)
   3. [Running the Container](#running-the-container)
5. [How It Works](#how-it-works)
6. [Contributing](#contributing)
7. [License](#license)

---

## Problem

I had to submit multiple PDF files to my college for one of their registration processes and so wanted to combine the files into a single PDF file. Unfortunately they all had security features enabled preventing editing or combining the files.

To work around this, I created a simple Python script that removes the invisible owner-only password and re-writes each document as an unlocked PDF. I then Dockerized the solution so that anyone can run it without installing Python dependencies on their host machine.

---

## Solution

I wrote a small Python script (`remove_pdf_security.py`) using PyPDF2 to:

1. Look through every `*.pdf` in `./data/`
2. Attempt decryption with an empty string (`""`)—which succeeds for owner-locked (permissions) PDFs that have no user password
3. Re-write each file, without any encryption, into `./processed/` under the original filename

Because I didn’t want to install Python and PyPDF2 on every machine I use (or remember which version I’m on), I bundled the script into a Docker image. This means you can drop your PDFs into a local `data/` folder and run:

```bash
$ docker build -t pdfdecrypter .
$ docker run --rm \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/processed:/app/processed" \
    pdfdecrypter
```

Everything happens inside the container. Your host machine stays clean, and in seconds you’ll have unlocked copies in `./processed/`.

---

## Project Structure

```
.
├── Dockerfile
├── README.md
├── remove_pdf_security.py
├── data/             ← Put your “locked” PDFs here
│   ├── file1.pdf
│   └── file2.pdf
└── processed/        ← Decrypted PDFs will be written here
│   ├── file1.pdf
│   └── file2.pdf
```

* **remove\_pdf\_security.py**: The Python script that reads `./data/*.pdf`, removes owner-only encryption, and writes decrypted files into `./processed/`.
* **Dockerfile**: Defines a lightweight Python container (based on `python:3.11-slim`), installs `PyPDF2` and `pycryptodome`, copies in the script, and sets it as the entrypoint.
* **data/**: A folder you create on your host. Drop your original PDFs here.
* **processed/**: An (initially empty) folder you create on your host. After running the container, you’ll find unlocked copies here.

---

## Setup & Usage

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop) (on Windows or macOS) or Docker Engine (on Linux) installed and running.
* A local `data/` directory containing the PDFs you wish to decrypt.
* An (optional but recommended) local `processed/` directory for output.

### Building the Docker Image

From your project’s root directory (where `Dockerfile` and `remove_pdf_security.py` live), run:

```bash
docker build -t pdfdecrypter .
```

* `-t pdfdecrypter` tags the resulting image so you can reference it easily.
* This will download a minimal Python base image, install `PyPDF2` and `pycryptodome`, copy in the script, and prepare the container to run it.

### Running the Container

Once the image is built, you can decrypt all your PDFs in one go:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/processed:/app/processed" \
  pdfdecrypter
```

Explanation:

* `--rm`: Automatically removes the container when it finishes.
* `-v "$(pwd)/data:/app/data"`: Mounts your host’s `./data` folder into `/app/data` inside the container.
* `-v "$(pwd)/processed:/app/processed"`: Mounts your host’s `./processed` folder into `/app/processed` inside the container.
* `pdfdecrypter`: The name of the Docker image we built.

After the script runs, check your local `./processed/` folder. You should see files like:

```
processed/
├── paystub1.pdf
├── paystub2.pdf
└── ...
```

Each matches the original filenames under `data/` but is now unlocked for merging or editing.

---

## How It Works

1. **Scanning for PDFs**
   The script sets `INPUT_DIR = "./data"` and uses `glob.glob("./data/*.pdf")` to find every PDF in that folder.
2. **Attempting Decryption**
   For each PDF, `PdfReader(input_path)` loads the file. If it’s encrypted, `reader.decrypt("")` tries an empty password. Many “owner-password-only” files allow that.
3. **Re-writing with No Encryption**
   If decryption succeeds (or the PDF was never encrypted), the script copies every page into a fresh `PdfWriter()` instance. Calling `writer.write(output_path)` writes a brand-new PDF without any encryption flags.
4. **Preserving Filenames**
   Instead of appending `_unlocked`, the script writes the output as `./processed/<original-filename>.pdf`. If a file with that name already exists, the script skips it to avoid overwriting.

Because everything runs inside Docker, you never need to install Python or its dependencies on your host. Simply rebuild or pull this container image whenever there’s an update.

---

## Contributing

I consider this to be a completed mini-project. Please feel free to use it, and if you would like to expand on the functionality, you are welcome to fork the project. I hope you find it helpful.

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.