# Intel Edge AI SW Developer Academy


## Clone

```
git clone https://github.com/<내계정>/kcci.intel.ai.project.git

또는

git clone git@github.com:<내계정>/kcci.intel.ai.project.git
```

## 환경설정
```
git config --global user.name "내 이름"
git config --global user.email "내@이메일.계정"
```


## Sync from Forked Repository
Fork한 개인 repo에서 upstream project를 sync하는 방법

```
cd kcci.intel.ai.project

git remote add upstream https://github.com/mokiya/kcci.intel.ai.project.git
git fetch upstream
git merge upstream/main
```