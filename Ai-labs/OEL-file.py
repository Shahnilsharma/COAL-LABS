"""
=====================================================================
 ZIAUDDIN UNIVERSITY - College of Computing & Software Engineering
 Artificial Intelligence & Machine Learning Lab
 Open-Ended Lab: Intelligent Campus Navigation and Search System
 Algorithms: DFS (stack + recursion), BFS, DLS, IDS
 Student: Shahnil
=====================================================================
"""

from collections import deque


# =====================================================================
# PART J - DATA STRUCTURES (Stack = LIFO, Queue = FIFO)
# =====================================================================

class Stack:
    """LIFO structure used by DFS and DLS."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def contents(self):
        """Node names currently inside the stack (for trace printing)."""
        return [node for node, path in self.items]


class Queue:
    """FIFO structure used by BFS."""

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.popleft()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def contents(self):
        return [node for node, path in self.items]


# =====================================================================
# PART B - CLASS 1 : Location
# =====================================================================

class Location:
    """A single point on the campus map."""

    def __init__(self, name, location_type="General", status="OPEN"):
        self.name = name
        self.location_type = location_type
        self.status = status          # OPEN or BLOCKED (Challenge 2)

    def is_open(self):
        return self.status == "OPEN"

    def display_location(self):
        print(f"  {self.name:<22} | {self.location_type:<14} | {self.status}")


class SearchResult:
    """Stores the statistics of one search run (Part K)."""

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.found = False
        self.path = []
        self.visited_count = 0
        self.goal_depth = -1
        self.iterations = 1           # used by IDS
        self.traversal = []

    def path_length(self):
        return len(self.path)

    def display(self):
        print("\n--------------- SEARCH RESULT ---------------")
        print(f"Algorithm      : {self.algorithm}")
        if self.found:
            print("Search Result  : GOAL FOUND!")
            print("Path           : " + " -> ".join(self.path))
            print(f"Path Length    : {self.path_length()} locations")
            print(f"Goal Depth     : {self.goal_depth}")
        else:
            print("Search Result  : GOAL NOT FOUND")
        print(f"Nodes Visited  : {self.visited_count}")
        print("---------------------------------------------")

    def show_vertical_path(self):
        """Part H - complete path reconstruction."""
        if not self.found:
            return
        print("\nComplete Route:")
        for i, node in enumerate(self.path):
            print(f"   {node}")
            if i != len(self.path) - 1:
                print("     |")
                print("     v")


# =====================================================================
# PART B - CLASS 2 : CampusMap   (PART C - adjacency list graph)
# =====================================================================

class CampusMap:

    def __init__(self, name="Ziauddin University Campus"):
        self.name = name
        self.locations = {}           # name -> Location object
        self.graph = {}               # name -> list of neighbour names
        self.history = []             # list of SearchResult objects

    # ------------------------- PART L : dynamic modification ---------
    def add_location(self, name, location_type="General"):
        if name in self.locations:
            print(f"[!] Location '{name}' already exists.")
            return False
        self.locations[name] = Location(name, location_type)
        self.graph[name] = []
        print(f"[+] Location added: {name} ({location_type})")
        return True

    def add_connection(self, a, b):
        if a not in self.graph or b not in self.graph:
            print("[!] Both locations must exist before connecting them.")
            return False
        if b in self.graph[a]:
            print("[!] Connection already exists.")
            return False
        self.graph[a].append(b)       # undirected graph
        self.graph[b].append(a)
        print(f"[+] Connection added: {a} <--> {b}")
        return True

    def set_status(self, name, status):
        if name not in self.locations:
            print("[!] Location not found.")
            return False
        self.locations[name].status = status
        print(f"[+] {name} is now {status}")
        return True

    # ------------------------- display -------------------------------
    def display_locations(self):
        print("\n=============== CAMPUS LOCATIONS ===============")
        print(f"  {'NAME':<22} | {'TYPE':<14} | STATUS")
        print("  " + "-" * 48)
        for loc in self.locations.values():
            loc.display_location()
        print(f"\n  Total Locations : {len(self.locations)}")
        print(f"  Total Connections: {self.count_edges()}")
        print("================================================")

    def display_graph(self):
        print("\n============== CAMPUS MAP (ADJACENCY LIST) ==============")
        for node in self.graph:
            flag = "" if self.locations[node].is_open() else "  [BLOCKED]"
            print(f"  {node:<20} -> {', '.join(self.graph[node])}{flag}")
        print("=========================================================")

    def count_edges(self):
        return sum(len(v) for v in self.graph.values()) // 2

    def neighbours(self, node):
        """Open neighbours only - blocked corridors are skipped."""
        return [n for n in self.graph[node] if self.locations[n].is_open()]

    def validate(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("[!] Invalid location name. Use option 9 to list locations.")
            return False
        return True

    # =================================================================
    # PART D - DFS USING AN EXPLICIT STACK  (with trace)
    # =================================================================
    def dfs(self, start, goal, trace=True):
        result = SearchResult("DFS (Stack)")
        stack = Stack()
        stack.push((start, [start]))
        visited = set()               # PART I - cycle detection

        if trace:
            print("\nDFS Stack Trace (LIFO):")

        while not stack.is_empty():
            if trace:
                print(f"  Stack: {stack.contents()}")
            node, path = stack.pop()

            if node in visited:       # already expanded -> cycle guard
                continue
            visited.add(node)
            result.traversal.append(node)
            result.visited_count += 1

            if node == goal:
                result.found = True
                result.path = path
                result.goal_depth = len(path) - 1
                break

            # reversed() keeps the left-most neighbour on top of the stack
            for nb in reversed(self.neighbours(node)):
                if nb not in visited:
                    stack.push((nb, path + [nb]))

        if trace:
            print("\nDFS Traversal Order:")
            print("  " + " -> ".join(result.traversal))
        self.history.append(result)
        return result

    # ---------------- DFS - recursive version (same logic) -----------
    def dfs_recursive(self, start, goal):
        result = SearchResult("DFS (Recursion)")
        visited = set()

        def explore(node, path):
            visited.add(node)
            result.traversal.append(node)
            result.visited_count += 1
            if node == goal:
                result.found = True
                result.path = path
                result.goal_depth = len(path) - 1
                return True
            for nb in self.neighbours(node):
                if nb not in visited:
                    if explore(nb, path + [nb]):
                        return True
            return False              # backtrack

        explore(start, [start])
        print("\nDFS (Recursive) Traversal Order:")
        print("  " + " -> ".join(result.traversal))
        self.history.append(result)
        return result

    # =================================================================
    # PART E - BFS USING A QUEUE
    # =================================================================
    def bfs(self, start, goal, trace=True):
        result = SearchResult("BFS (Queue)")
        queue = Queue()
        queue.enqueue((start, [start]))
        visited = {start}             # PART I - cycle detection

        if trace:
            print("\nBFS Queue Trace (FIFO):")

        while not queue.is_empty():
            if trace:
                print(f"  Queue: {queue.contents()}")
            node, path = queue.dequeue()
            result.traversal.append(node)
            result.visited_count += 1

            if node == goal:
                result.found = True
                result.path = path    # first hit = shortest path
                result.goal_depth = len(path) - 1
                break

            for nb in self.neighbours(node):
                if nb not in visited:
                    visited.add(nb)
                    queue.enqueue((nb, path + [nb]))

        if trace:
            print("\nBFS Traversal Order:")
            print("  " + " -> ".join(result.traversal))
        self.history.append(result)
        return result

    # =================================================================
    # PART F - DEPTH LIMITED SEARCH
    # =================================================================
    def dls(self, start, goal, limit, verbose=True, record=True):
        result = SearchResult(f"DLS (limit={limit})")

        def recurse(node, goal, depth, path, visited):
            result.traversal.append(node)
            result.visited_count += 1
            if node == goal:
                result.found = True
                result.path = path
                result.goal_depth = depth
                return True
            if depth == limit:        # depth limit reached -> stop going deeper
                return False
            visited.add(node)
            for nb in self.neighbours(node):
                if nb not in visited:
                    if recurse(nb, goal, depth + 1, path + [nb], visited):
                        return True
            visited.remove(node)      # allow other branches to reuse the node
            return False

        recurse(start, goal, 0, [start], set())

        if verbose:
            print(f"\nDLS Traversal Order (Depth Limit = {limit}):")
            print("  " + " -> ".join(result.traversal))
            if not result.found:
                print("\nGoal Not Found")
                print("Reason: Destination is beyond the depth limit.")
        if record:
            self.history.append(result)
        return result

    # =================================================================
    # PART G - ITERATIVE DEEPENING SEARCH
    # =================================================================
    def ids(self, start, goal, max_depth=10):
        final = SearchResult("IDS")
        total_visited = 0

        for depth in range(max_depth + 1):
            print(f"Searching at Depth = {depth}")
            attempt = self.dls(start, goal, depth, verbose=False, record=False)
            total_visited += attempt.visited_count
            print(f"  Nodes expanded at this depth: {attempt.visited_count}")

            if attempt.found:
                print("  Goal Found!")
                final.found = True
                final.path = attempt.path
                final.goal_depth = attempt.goal_depth
                final.traversal = attempt.traversal
                final.iterations = depth + 1
                break
            print("  Goal Not Found")

        final.visited_count = total_visited
        if final.found:
            print("\nIDS Traversal Order (successful iteration):")
            print("  " + " -> ".join(final.traversal))
            print(f"Total Iterations Performed: {final.iterations}")
        self.history.append(final)
        return final

    # =================================================================
    # PART K - PERFORMANCE COMPARISON TABLE
    # =================================================================
    def comparison_table(self):
        if not self.history:
            print("[!] No searches performed yet.")
            return
        print("\n=================== SEARCH COMPARISON TABLE ===================")
        print(f"{'ALGORITHM':<18}{'VISITED':<10}{'DEPTH':<8}{'PATH LEN':<10}{'RESULT':<10}")
        print("-" * 62)
        for r in self.history:
            depth = r.goal_depth if r.found else "-"
            plen = r.path_length() if r.found else "-"
            status = "Found" if r.found else "Not Found"
            print(f"{r.algorithm:<18}{r.visited_count:<10}{str(depth):<8}"
                  f"{str(plen):<10}{status:<10}")
        print("=" * 62)

        best = [r for r in self.history if r.found]
        if best:
            fewest = min(best, key=lambda r: r.visited_count)
            shortest = min(best, key=lambda r: r.path_length())
            print(f"Fewest nodes visited : {fewest.algorithm} ({fewest.visited_count})")
            print(f"Shortest path found  : {shortest.algorithm} "
                  f"({shortest.path_length()} locations)")

    # ------------------- Challenge 5 : recommendation ----------------
    @staticmethod
    def recommend(situation):
        table = {
            "1": ("BFS", "BFS expands level by level, so the first solution "
                         "found is the shortest path in an unweighted graph."),
            "2": ("DFS", "DFS only stores the current branch, so its memory "
                         "requirement is O(depth) instead of O(breadth^depth)."),
            "3": ("DLS", "When the maximum useful depth is known, DLS avoids "
                         "wasting time on deeper useless branches."),
            "4": ("IDS", "IDS needs no prior knowledge of the goal depth and "
                         "still keeps DFS memory with BFS optimality."),
        }
        return table.get(situation)


# =====================================================================
# DEFAULT CAMPUS (PART C : 11 locations, 14 connections, 3 cycles)
# =====================================================================

def build_default_campus():
    campus = CampusMap()

    data = [
        ("Main Gate", "Entrance"),
        ("Reception", "Service"),
        ("Parking Area", "Utility"),
        ("Library", "Academic"),
        ("Administration", "Office"),
        ("CS Department", "Academic"),
        ("AI Laboratory", "Laboratory"),
        ("Cafeteria", "Facility"),
        ("Auditorium", "Facility"),
        ("Examination Hall", "Academic"),
        ("Emergency Exit", "Safety"),
    ]
    for name, kind in data:
        campus.locations[name] = Location(name, kind)
        campus.graph[name] = []

    edges = [
        ("Main Gate", "Reception"),
        ("Main Gate", "Parking Area"),
        ("Reception", "Library"),
        ("Reception", "Administration"),
        ("Library", "Cafeteria"),
        ("Library", "Main Gate"),            # cycle 1
        ("Administration", "CS Department"),
        ("CS Department", "AI Laboratory"),
        ("AI Laboratory", "Examination Hall"),
        ("AI Laboratory", "Emergency Exit"),
        ("Parking Area", "Auditorium"),
        ("Parking Area", "Emergency Exit"),
        ("Auditorium", "Examination Hall"),  # cycle 2
        ("Auditorium", "Cafeteria"),         # cycle 3
    ]
    for a, b in edges:
        campus.graph[a].append(b)
        campus.graph[b].append(a)

    return campus


# =====================================================================
# PART A - MENU DRIVEN INTERFACE (input, output, loops, conditions)
# =====================================================================

def print_menu():
    print("\n=========================================")
    print("   INTELLIGENT CAMPUS NAVIGATION SYSTEM")
    print("=========================================")
    print(" 1. Add Location")
    print(" 2. Add Connection")
    print(" 3. Display Campus Map")
    print(" 4. DFS Search")
    print(" 5. BFS Search")
    print(" 6. DLS Search")
    print(" 7. IDS Search")
    print(" 8. Display Search Comparison")
    print(" 9. Display Locations")
    print("10. Block / Unblock a Location")
    print("11. Emergency Mode")
    print("12. Multiple Destination Search")
    print("13. Algorithm Recommendation")
    print("14. Exit")
    print("=========================================")


def ask_route(campus):
    source = input("Enter starting location: ").strip()
    destination = input("Enter destination: ").strip()
    if not campus.validate(source, destination):
        return None, None
    print(f"\nStarting Location: {source}")
    print(f"Destination: {destination}")
    return source, destination


def main():
    campus = build_default_campus()
    print("\nWelcome, Shahnil. Campus graph loaded successfully.")
    print(f"Locations: {len(campus.locations)} | "
          f"Connections: {campus.count_edges()}")

    running = True
    while running:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter new location: ").strip()
            kind = input("Enter location type: ").strip() or "General"
            campus.add_location(name, kind)

        elif choice == "2":
            a = input("Enter first location: ").strip()
            b = input("Connect it with: ").strip()
            campus.add_connection(a, b)

        elif choice == "3":
            campus.display_graph()

        elif choice == "4":
            s, d = ask_route(campus)
            if s:
                mode = input("Use (1) Stack or (2) Recursion? ").strip()
                if mode == "2":
                    r = campus.dfs_recursive(s, d)
                else:
                    r = campus.dfs(s, d)
                r.display()
                r.show_vertical_path()

        elif choice == "5":
            s, d = ask_route(campus)
            if s:
                r = campus.bfs(s, d)
                r.display()
                r.show_vertical_path()

        elif choice == "6":
            s, d = ask_route(campus)
            if s:
                limit = int(input("Enter depth limit: ").strip())
                r = campus.dls(s, d, limit)
                r.display()
                r.show_vertical_path()

        elif choice == "7":
            s, d = ask_route(campus)
            if s:
                print()
                r = campus.ids(s, d)
                r.display()
                r.show_vertical_path()

        elif choice == "8":
            campus.comparison_table()

        elif choice == "9":
            campus.display_locations()

        elif choice == "10":
            name = input("Enter location name: ").strip()
            state = input("Set status (OPEN / BLOCKED): ").strip().upper()
            campus.set_status(name, state)

        elif choice == "11":
            current = input("Current Location: ").strip()
            exits = [n for n, l in campus.locations.items()
                     if l.location_type in ("Safety", "Entrance")]
            print(f"Available emergency exits: {', '.join(exits)}")
            best = None
            for e in exits:
                r = campus.bfs(current, e, trace=False)
                if r.found and (best is None or
                                r.path_length() < best.path_length()):
                    best = r
            if best:
                print("\n*** EMERGENCY ROUTE ***")
                best.display()
                best.show_vertical_path()
            else:
                print("[!] No safe route available.")

        elif choice == "12":
            start = input("Enter starting location: ").strip()
            targets = input("Enter destinations (comma separated): ").split(",")
            for t in targets:
                t = t.strip()
                if campus.validate(start, t):
                    r = campus.bfs(start, t, trace=False)
                    status = " -> ".join(r.path) if r.found else "No route"
                    print(f"  {start} => {t:<18} : {status}")

        elif choice == "13":
            print("\n1. Shortest path required")
            print("2. Memory is limited")
            print("3. Maximum search depth is known")
            print("4. Goal depth is unknown")
            pick = input("Select your situation: ").strip()
            rec = CampusMap.recommend(pick)
            if rec:
                print(f"\nRecommended: {rec[0]}")
                print(f"Justification: {rec[1]}")
            else:
                print("[!] Invalid situation.")

        elif choice == "14":
            print("\nExiting Intelligent Campus Navigation System. Goodbye!")
            running = False

        else:
            print("[!] Invalid choice. Please enter 1 - 14.")


if __name__ == "__main__":
    main()
