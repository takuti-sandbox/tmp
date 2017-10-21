package main

import (
	"container/heap"
	"fmt"
	"math/rand"
)

type Item struct {
	ID    int
	Score float32
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].Score > pq[j].Score
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*Item)
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	*pq = old[0 : n-1]
	return item
}

func getTopItems(items []Item, limit int) []Item {
	n := len(items)

	pq := make(PriorityQueue, n)
	for i := 0; i < n; i++ {
		pq[i] = &items[i]
	}
	heap.Init(&pq)

	if n < limit {
		limit = n
	}
	items = make([]Item, limit)
	for i := 0; i < limit; i++ {
		items[i] = *heap.Pop(&pq).(*Item)
	}

	return items
}

func main() {
	n := 100
	items := make([]Item, n)
	for i := 0; i < n; i++ {
		items[i] = Item{
			ID:    i,
			Score: rand.Float32(),
		}
	}

	limit := 10
	topItems := getTopItems(items, limit)
	for i := 0; i < limit; i++ {
		item := topItems[i]
		fmt.Printf("%3d: %f\n", item.ID, item.Score)
	}
}
