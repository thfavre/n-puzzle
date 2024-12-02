from heuristic import Heuristic
from typing import List, Optional, Tuple
from functools import lru_cache

class Node:
	"""
	A class representing a node in the search tree for solving the N-puzzle.
	"""

	def __init__(self, parentNode: Optional['Node'], grid: List[int], solutionGrid: List[int], gridSize: int, heuristic: str, searchStrategy: str = 'a_star') -> None:
		"""
		Initialize a Node with the given attributes.

		Args:
			parentNode (Optional[Node]): The parent node leading to this node.
			grid (List[int]): The current state of the puzzle.
			solutionGrid (List[int]): The goal state of the puzzle.
			gridSize (int): The size of the puzzle grid (e.g., 3 for a 3x3 puzzle).
			heuristic (str): The heuristic method to use for evaluating the node.
			searchStrategy (str): The type of search algorithm ('a_star', 'uniform', 'greedy').
		"""
		self._parentNode: Optional['Node'] = parentNode
		self._grid: List[int] = grid
		self._gridSize: int = gridSize
		self._heuristic: str = heuristic
		self._searchType: str = searchStrategy
		self._level: int = 0 if not parentNode else parentNode.getLevel() + 1

		# Calculate the cost based on the type of search
		self._g_cost: int = self._level
		self._h_cost: int = Heuristic.evaluate(self, solutionGrid, gridSize, self._heuristic)

		if self._searchType == 'a_star':
			self._cost = self._g_cost + self._h_cost * 2  # g(x) + h(x) * 2
		elif self._searchType == 'uniform':
			self._cost = self._g_cost  # Only g(x)
		elif self._searchType == 'greedy':
			self._cost = self._h_cost  # Only h(x)
		else:
			raise ValueError(f"Unsupported search type: {self._searchType}")

	def showGrid(self) -> None:
		"""
		Print the current state of the puzzle grid in a formatted way.
		"""
		w: int = len(str(self._gridSize * self._gridSize)) + 1
		for i, nb in enumerate(self._grid):
			print(str(nb).rjust(w), end="")
			if ((i + 1) % self._gridSize == 0):
				print()

	def __lt__(self, other: 'Node') -> bool:
		"""
		Compare this node with another node based on their cost.

		Args:
			other (Node): Another node to compare against.

		Returns:
			bool: True if this node's cost is less than the other node's cost, False otherwise.
		"""
		return self._cost < other._cost

	def createChildrenNodes(self, solutionGrid: List[int], gridSize: int) -> List['Node']:
		"""
		Generate and yield a list of child nodes by moving the empty tile (0) in all possible directions.

		Args:
			solutionGrid (List[int]): The goal state of the puzzle.
			gridSize (int): The size of the puzzle grid (e.g., 3 for a 3x3 puzzle).

		Yields:
        	Node: A new node generated by moving the empty tile.
		"""
		newNodes: List['Node'] = []
		zeroX: int = self._grid.index(0) % gridSize
		zeroY: int = self._grid.index(0) // gridSize

		# Move the 0 to the right
		if zeroX < gridSize - 1:
			newGrid: List[int] = self._grid.copy()
			newGrid[zeroY * gridSize + zeroX], newGrid[zeroY * gridSize + zeroX + 1] = \
				newGrid[zeroY * gridSize + zeroX + 1], newGrid[zeroY * gridSize + zeroX]
			yield Node(self, newGrid, solutionGrid, gridSize, self._heuristic, self._searchType)

		# Move the 0 to the left
		if zeroX > 0:
			newGrid = self._grid.copy()
			newGrid[zeroY * gridSize + zeroX], newGrid[zeroY * gridSize + zeroX - 1] = \
				newGrid[zeroY * gridSize + zeroX - 1], newGrid[zeroY * gridSize + zeroX]
			yield Node(self, newGrid, solutionGrid, gridSize, self._heuristic, self._searchType)

		# Move the 0 to the bottom
		if zeroY < gridSize - 1:
			newGrid = self._grid.copy()
			newGrid[zeroY * gridSize + zeroX], newGrid[zeroY * gridSize + zeroX + gridSize] = \
				newGrid[zeroY * gridSize + zeroX + gridSize], newGrid[zeroY * gridSize + zeroX]
			yield Node(self, newGrid, solutionGrid, gridSize, self._heuristic, self._searchType)

		# Move the 0 to the top
		if zeroY > 0:
			newGrid = self._grid.copy()
			newGrid[zeroY * gridSize + zeroX], newGrid[zeroY * gridSize + zeroX - gridSize] = \
				newGrid[zeroY * gridSize + zeroX - gridSize], newGrid[zeroY * gridSize + zeroX]
			yield Node(self, newGrid, solutionGrid, gridSize, self._heuristic, self._searchType)

	# Getters
	def getParentNode(self) -> Optional['Node']:
		return self._parentNode

	def getGrid(self) -> List[int]:
		return self._grid

	def getGridSize(self) -> int:
		return self._gridSize

	def getLevel(self) -> int:
		return self._level

	def getCost(self) -> int:
		return self._cost

	@staticmethod
	@lru_cache(None)
	def getCoordinates(index: int, size: int) -> Tuple[int, int]:
		"""Get the (x, y) coordinates for a given index in the grid."""
		return index % size, index // size
