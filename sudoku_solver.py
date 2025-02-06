import cv2
import numpy as np
import pytesseract

def extract_sudoku_grid(image_path):
    # Image load karo
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold lagao
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Contours dhoondo
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    sudoku_contour = contours[0]
    
    # Shape approx karlo
    peri = cv2.arcLength(sudoku_contour, True)
    approx = cv2.approxPolyDP(sudoku_contour, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    
    # Grid crop karo
    return gray[y:y+h, x:x+w]

def extract_numbers_from_grid(sudoku_grid_img):
    cell_size = sudoku_grid_img.shape[0] // 9
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    for i in range(9):
        for j in range(9):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size
            cell = sudoku_grid_img[y1:y2, x1:x2]
            
            # Empty check
            if cell.size == 0:
                continue
            
            # OCR ke liye resize & threshold
            cell = cv2.resize(cell, (28, 28))
            cell = cv2.threshold(cell, 150, 255, cv2.THRESH_BINARY_INV)[1]
            
            # Digit dhoondo
            text = pytesseract.image_to_string(cell, config='--oem 3 --psm 10 outputbase digits')
            text = text.strip()
            
            if text.isdigit():
                grid[i][j] = int(text)
    
    return grid

def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    box_x, box_y = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[box_x + i][box_y + j] == num:
                return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def print_karo(image_path):
    sudoku_grid_img = extract_sudoku_grid(image_path)
    sudoku_grid = extract_numbers_from_grid(sudoku_grid_img)
    
    print("Extracted Sudoku Grid : ")
    for row in sudoku_grid:
        print(row)
    
    if solve_sudoku(sudoku_grid):
        print("\nSolved Sudoku Grid : ")
        for row in sudoku_grid:
            print(row)
    else:
        print("\nNo solution found")

# Run karo
image_path = "sudoku_10.png" 
print_karo(image_path)
