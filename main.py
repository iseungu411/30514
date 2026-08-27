import json
import os
from datetime import datetime


class TaskManager:

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """JSON 파일에서 일정 데이터를 불러옵니다."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 데이터 불러오기 실패: {e}")
                return []
        return []

    def save_tasks(self):
        """일정 데이터를 JSON 파일에 저장합니다."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 데이터 저장 실패: {e}")

    def add_task(self, title, category, priority):
        """새로운 일정을 추가합니다."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "category": category,
            "priority": priority,  # 높음, 보통, 낮음
            "status": "미완료",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"\n✅ '{title}' 할 일이 성공적으로 등록되었습니다.")

    def view_tasks(self):
        """등록된 전체 일정을 출력합니다."""
        if not self.tasks:
            print("\n📌 등록된 할 일이 없습니다.")
            return

        print("\n" + "=" * 65)
        print(
            f"{'ID':<4} | {'카테고리':<10} | {'중요도':<6} | {'상태':<8} | {'할 일 내용'}"
        )
        print("=" * 65)

        for task in self.tasks:
            status_icon = "🟢" if task["status"] == "완료" else "🔴"
            print(
                f"{task['id']:<4} | {task['category']:<10} | {task['priority']:<6} | {status_icon} {task['status']:<6} | {task['title']}"
            )
        print("=" * 65)

    def complete_task(self, task_id):
        """특정 일정을 완료 상태로 변경합니다."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "완료"
                self.save_tasks()
                print(f"\n🎉 ID {task_id}번 할 일을 완료 처리했습니다!")
                return
        print("\n❌ 해당 ID의 할 일을 찾을 수 없습니다.")

    def delete_task(self, task_id):
        """특정 일정을 삭제합니다."""
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                # ID 재정렬
                for idx, t in enumerate(self.tasks, start=1):
                    t["id"] = idx
                self.save_tasks()
                print(f"\n🗑️ ID {task_id}번 할 일을 삭제했습니다.")
                return
        print("\n❌ 해당 ID의 할 일을 찾을 수 없습니다.")


def main():
    manager = TaskManager()

    while True:
        print("\n[ 📋 스마트 일정 및 학습 관리 시스템 ]")
        print("1. 전체 할 일 보기")
        print("2. 새 할 일 추가")
        print("3. 할 일 완료 처리")
        print("4. 할 일 삭제")
        print("5. 종료")

        choice = input("\n원하는 작업의 번호를 입력하세요 (1-5): ").strip()

        if choice == "1":
            manager.view_tasks()
        elif choice == "2":
            title = input("할 일 내용을 입력하세요: ").strip()
            category = input(
                "카테고리 (예: 공부, 동아리, 개인): "
            ).strip()
            priority = input(
                "중요도 (높음 / 보통 / 낮음): "
            ).strip()
            if title and category and priority:
                manager.add_task(title, category, priority)
            else:
                print("\n⚠️ 모든 항목을 정확히 입력해주세요.")
        elif choice == "3":
            try:
                task_id = int(
                    input("완료할 할 일의 ID를 입력하세요: ").strip()
                )
                manager.complete_task(task_id)
            except ValueError:
                print("\n⚠️ 숫자로 된 ID를 입력해주세요.")
        elif choice == "4":
            try:
                task_id = int(
                    input("삭제할 할 일의 ID를 입력하세요: ").strip()
                )
                manager.delete_task(task_id)
            except ValueError:
                print("\n⚠️ 숫자로 된 ID를 입력해주세요.")
        elif choice == "5":
            print("\n프로그램을 종료합니다. 좋은 하루 되세요!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 1번부터 5번 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
