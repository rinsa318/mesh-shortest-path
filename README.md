# find_mesh_shortest_path
指定した頂点間の最短経路(三角形の辺を通る経路)を求めるコード．  

最短経路を示す頂点のインデックス(.txt)と，最短経路で囲まれた領域でオブジェクトをカットしたもの(.obj)が保存される．


<img src="./test/example-figure.png" width=50%>


## How to run

```
python3 main.py argvs[1] argvs[2]

argvs[1] : 最短経路を求めたい.objファイルへのパス(上図だとグレーのメッシュ)
argvs[2] : 求めたい頂点のインデックスが書かれた.txtファイルへのパス(上図だと青い点のインデックスが書かれたファイル)
```


## Example

```
python main.py ./test/test.obj ./test/test_fp.txt
```

以下が保存

```
./test/test_fp/inside.obj --> 上図の赤線内の領域
./test/test_fp/shortest-path.txt --> 上図の赤線のインデックス
```
