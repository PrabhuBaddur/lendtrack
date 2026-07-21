from datetime import datetime
from database import get_connection
from collections import Counter,defaultdict

def merge(left,right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i]<= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j +=1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(items):
    if len(items)<=1:
        return items
    mid = len(items)//2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return merge(left,right)

def binary_search(sorted_list,target):
    lo = 0
    hi = len(sorted_list) - 1


    while lo<=hi:
        mid = (lo + hi)//2

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            lo = mid+1
        else:
            hi = mid - 1

    return -1 

    
def stream_overdue_loans():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM transactions WHERE returned_at IS NULL").fetchall()

    
    now = datetime.utcnow()
    for row in rows:
        due = datetime.fromisoformat(row["due_date"])
        if now > due:
            yield dict(row)

def most_borrowed_books(top = 5):
    with get_connection() as conn:
        rows = conn.execute("SELECT book_id FROM transactions").fetchall()

    counts = Counter(row["book_id"] for row in rows)
    return counts.most_common(top)

def loans_grouped_by_member():
    with get_connection() as conn:
        rows = conn.execute("SELECT member_id,book_id FROM transactions").fetchall()

    grouped = defaultdict(list)

    for row in rows:
        grouped[row["member_id"]].append(row["book_id"])
    return dict(grouped)