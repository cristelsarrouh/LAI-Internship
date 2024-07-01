# T Cell Literature Analysis with AI/Text-Mining Tools

This project represents the work conducted during my M2 Internship at the Adhesion & Inflammation Lab. The focus was on gaining a deep understanding of early T cell literature through the use of AI and text-mining tools. The primary goal was to select relevant articles related to our topic of interest, fetch the associated metadata and PDFs, store them, and extract text from these PDFs. This extracted text is then used as input for Large Language Models (LLMs) to facilitate information retrieval from the scientific literature.

## Overview

This project aims to provide a semi-automated pipeline and developed scripts to:

1. Select relevant articles on early T cell research.
2. Fetch metadata and download associated PDFs.
3. Store and extract text from these PDFs.
4. Use extracted text as input for LLMs to enhance literature search capabilities.

## Project Structure

The project is organized into five main directories:

1. **Analysis**: Contains scripts for extracting citations, localizing text, and other analyses.
2. **Metadata & PDFs**: Scripts for fetching metadata and downloading PDFs.
3. **Visualization**: Code for plotting and visualizing the results of our analysis.
4. **Text Extraction Tests**: Tests using various Python libraries for text extraction, which were found to be suboptimal.
5. **Text Extraction Tools**: Scripts developed for extracting text from PDFs using three tools: `pdfminer.six`, `LLamaIndex`, and `GROBID`.
