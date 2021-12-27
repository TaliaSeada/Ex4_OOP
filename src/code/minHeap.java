package code;

/**
 * this class builds a minHeap for the Dijkstra algorithm
 */
public class minHeap {
    int capacity;
    int currentSize;
    pair[] mH;
    int[] indexes; //will be used to decrease the distance


    public minHeap(int capacity) {
        this.capacity = capacity;
        mH = new pair[capacity + 1];
        indexes = new int[capacity];
        mH[0] = new pair();
        mH[0].dist = Integer.MIN_VALUE;
        mH[0].node = -1;
        currentSize = 0;
    }


    public void insert(pair x) {
        currentSize++;
        int idx = currentSize;
        mH[idx] = x;
        indexes[x.node] = idx;
        bubbleUp(idx);
    }

    public void bubbleUp(int pos) {
        int parentIdx = pos / 2;
        int currentIdx = pos;
        while (currentIdx > 0 && mH[parentIdx].dist > mH[currentIdx].dist) {
            pair currentNode = mH[currentIdx];
            pair parentNode = mH[parentIdx];

            //swap the positions
            indexes[currentNode.node] = parentIdx;
            indexes[parentNode.node] = currentIdx;
            swap(currentIdx, parentIdx);
            currentIdx = parentIdx;
            parentIdx = parentIdx / 2;
        }
    }

    public pair extractMin() {
        pair min = mH[1];
        pair lastNode = mH[currentSize];
// update the indexes[] and move the last node to the top
        indexes[lastNode.node] = 1;
        mH[1] = lastNode;
        mH[currentSize] = null;
        sinkDown(1);
        currentSize--;
        return min;
    }

    public void sinkDown(int k) {
        int smallest = k;
        int leftChildIdx = 2 * k;
        int rightChildIdx = 2 * k + 1;
        if (leftChildIdx < heapSize() && mH[smallest].dist > mH[leftChildIdx].dist) {
            smallest = leftChildIdx;
        }
        if (rightChildIdx < heapSize() && mH[smallest].dist > mH[rightChildIdx].dist) {
            smallest = rightChildIdx;
        }
        if (smallest != k) {

            pair smallestNode = mH[smallest];
            pair kNode = mH[k];

            //swap the positions
            indexes[smallestNode.node] = k;
            indexes[kNode.node] = smallest;
            swap(k, smallest);
            sinkDown(smallest);
        }
    }

    public void swap(int a, int b) {
        pair temp = mH[a];
        mH[a] = mH[b];
        mH[b] = temp;
    }

    public boolean isEmpty() {
        return currentSize == 0;
    }

    public int heapSize() {
        return currentSize;
    }
}