# AWS-S3-CloudFront-RDS
## Demo
http://test-1783064897.us-east-2.elb.amazonaws.com/
## 簡介
AWS S3 + AWS CloudFront + AWS RDS 雲端服務整合 <br><br>
### 1. 簡易的圖片庫 ( 上傳、刪除、下載 )：
  - AWS S3 儲存圖片
  - AWS CloudFront 建立 CDN 系統
  - AWS RDS 建立資料庫 <br><br>

![](https://github.com/ttiverson3/AWS-S3-CloudFront-RDS/blob/master/imgs/flowchart.png)

### 2. AWS Load Balancers
  - 利用 AWS Load Balancers 建立負載平衡架構 <br><br>
  <img src="https://github.com/ttiverson3/AWS-S3-CloudFront-RDS/blob/master/imgs/AWS-loader-balancers.png" width="740"/>
  
  - Avg. Response Time：1753ms -> 477ms ( 使用 loader.io 測試 )<br><br>
  <div align="center">
    <img src="https://github.com/ttiverson3/AWS-S3-CloudFront-RDS/blob/master/imgs/test.png" width="450" height="318"/>
    <img src="https://github.com/ttiverson3/AWS-S3-CloudFront-RDS/blob/master/imgs/test-load-balance.png" width="450" height="318"/>
  </div>
