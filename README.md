# Artificial_Intelligence Assignment_1 HCMUT Semester 202

## Member in Team
|NAME|ID Student|
|---|---|
|Lê Quang Tùng|1810784|
|Trương Công Thành|1810766|
|Vũ Minh Dương|1810885|
|Lê Long|1812881|

## Exercise 1 - N puzzle with DFS

[Code](https://github.com/OnceUponATimeMathley/CSE-Artificial_Intelligence_Assignment_1/blob/master/Exercise_1/N-puzzle-DFS.py)
### DFS with Recursion

#### Run Code
    # If you want the available input get in LIST_PUZZLE_DATA
    python3 N-puzzle-DFS.py (numRow = 3) noRandom (numMoves) Recursive 
    # If you want to generate random data
    python3 N-puzzle-DFS.py (numRow) Random (numMoves) Recursive

#### Pseudocode
    DFS(state): 
    # list_action: Lưu trữ các hướng trong lúc đệ quy 
    # Mục đích dùng để in kết quả 
    Đánh dấu state đã được duyệt 
    Nếu state là trạng thái kết thúc: 
        in kết quả theo list_action và dừng 
    Duyệt các hướng(dir) có thể trong LegalMoves(state): 
        # Trạng thái mới khi đi theo hướng (dir) 
        next_state = result(state, dir) 
        Nếu next_state chưa được duyêt: 
        Thêm dir vào list_action 
        DFS(next_state) 
        Xóa dir ra khỏi list_action
