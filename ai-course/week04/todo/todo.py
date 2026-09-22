import json
import os

# 파일 경로 설정
TODO_FILE = 'todo.json'

def load_tasks():
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def add_task(tasks):
    """새로운 할 일을 추가합니다."""
    task_name = input("추가할 할 일을 입력하세요: ").strip()
    if task_name:
        tasks.append({"task": task_name, "completed": False})
        save_tasks(tasks)
        print(f"'{task_name}'이(가) 추가되었습니다.")
    else:
        print("할 일 내용을 입력해야 합니다.")

def view_tasks(tasks):
    """할 일 목록을 보여줍니다."""
    if not tasks:
        print("\n현재 할 일 목록이 비어 있습니다.")
        return

    print("\n--- 할 일 목록 ---")
    for i, task in enumerate(tasks, 1):
        status = "[V]" if task['completed'] else "[ ]"
        print(f"{i}. {status} {task['task']}")
    print("------------------")

def complete_task(tasks):
    """할 일을 완료 상태로 표시합니다."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        choice = int(input("완료 처리할 번호를 입력하세요: "))
        if 1 <= choice <= len(tasks):
            tasks[choice - 1]['completed'] = True
            save_tasks(tasks)
            print(f"{tasks[choice - 1]['task']}를 완료로 표시했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해 주세요.")

def delete_task(tasks):
    """할 일을 삭제합니다."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        choice = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            save_tasks(tasks)
            print(f"'{removed['task']}'을(를) 삭제했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해 주세요.")

def main():
    """메인 메뉴 루프를 실행합니다."""
    tasks = load_tasks()

    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해 주세요.")

if __name__ == "__main__":
    main()
