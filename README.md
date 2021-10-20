# PathPlanning
RRT, RRT*, Dubins, RRT-Dubins

## RRT Algorithm
### RRT
- Rapidly exploring random tree

### 알고리즘 목표
- 시작점으로부터 목적지까지 도달하는 경로 생성

### Pseudocode
![스크린샷, 2021-10-20 18-49-30](https://user-images.githubusercontent.com/67509269/138074523-8acd360e-0493-4698-882e-d43d00be7382.png)

### 알고리즘 순서
![스크린샷, 2021-10-20 18-49-39](https://user-images.githubusercontent.com/67509269/138074569-495e84dd-43f2-41ce-aa34-8b700ee7cde0.png)

1. 랜덤 노드 설정
2. 랜덤 노드로부터 가장 가까운 노드 선택
3. 랜덤 노드로 향하는 방향(직선)으로 step 만큼 늘려 새로운 노드 생성
4. 장애물과 충돌 체크 후 (Euclidean distance 기반) 새로운 노드로 트리에 추가
5. 1~4 목적지에 도달할때까지 진행

### Result
![rrt_100](https://user-images.githubusercontent.com/67509269/138074610-5b16c7fe-6c64-4e40-9b5c-0d42655c0241.png)

## RRT* Algorithm
### Pseudocode
![스크린샷, 2021-10-20 18-55-01](https://user-images.githubusercontent.com/67509269/138074664-aea81450-1a4c-42d7-9a91-c2bfa9517ccc.png)

### 알고리즘 개선
- RRT*는 RRT와 다르게 트리 내의 노드를 대체하여 cost를 줄일 수 있는 경우 기존 노드를 대체하여 트리를 구성
- 따라서 RRT보다 최적의 경로 생성

### 알고리즘 순서
![스크린샷, 2021-10-20 18-55-13](https://user-images.githubusercontent.com/67509269/138074688-27d0a7e6-e023-4373-8405-13ca090b738e.png)

1. 랜덤 노드 생성
2. 랜덤 노드로부터 가장 가까운 노드 선택
3. 랜덤노드로 향하는 방향으로 step만큼 늘려 새로운 노드 생성
4. 장애물과의 충돌 체크 후 (충돌이 없을 시)  
  4.1 새로운 노드로부터 가까운 노드들 선택(특정 반경 내)  
  4.2 가까운 노드들 중 lowest cost를 가진 노드를 새로운 노드와 연결하여 새로운 노드의 부모 노드로 설정  
  4.3 가까운 노드들 중 새로운 노드를 부모 노드로 할 때 더 낮은 cost를 갖는 노드가 있는지 탐색  
  4.4 있다면 트리 재구성 (rewiring) 진행  

### Result
![스크린샷, 2021-10-20 19-00-39](https://user-images.githubusercontent.com/67509269/138074709-1901acb9-1687-443f-8d66-4fe2322ff0a4.png)
![스크린샷, 2021-10-20 19-00-46](https://user-images.githubusercontent.com/67509269/138074714-0eb8517d-4609-4a2f-a957-82fe5b478141.png)

- RRT(왼쪽)과 RRT*(오른쪽)을 비교했을 때, 좀 더 효율적으로 연결
    - RRT  : 141 -> 362
    - RRT* : 399 -> 362

## Dubins path
### Dubins path
![스크린샷, 2021-10-20 18-43-15](https://user-images.githubusercontent.com/67509269/138074811-5aa907f8-527c-4872-bf63-de92b194f4e9.png)

- 두 점 (A, B)가 주어졌을때, curvature constraint를 고려하여 두 점을 잇는 shortest curve를 말함
- Forward 방향으로만 이동 가능하며 right, straight, left의 세 조합으로 구성
- Optimal path로 총 6 type 존재(RSR, RSL, LSR, LSL, RLR, LRL)

### Result
![스크린샷, 2021-10-20 19-09-49](https://user-images.githubusercontent.com/67509269/138074904-36bd82cd-658b-469d-8082-412d98e30631.png)
