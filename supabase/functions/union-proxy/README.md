# union-proxy (Supabase Edge Function)

GitHub Actions(Azure) egress IP가 성서유니온 서버(`sum.su.or.kr:8888`)에 간헐적으로
차단되는 문제를 우회하기 위한 얇은 프록시. 비-Azure + 임의 포트를 허용하는
Supabase Edge Function(Deno 런타임)에서 union을 대신 호출한다.

```
GitHub Actions ──> Supabase Edge Function ──> sum.su.or.kr:8888
   (Azure)         (비-Azure, 포트 8888 OK)
```

배포는 [`.github/workflows/deploy-proxy.yaml`](../../../.github/workflows/deploy-proxy.yaml)
가 담당한다. `index.ts` 가 main에 푸시되면 자동 배포된다.

## 1회성 설정

**A. 배포용 시크릿 (GitHub Actions)**

리포 **Settings → Secrets and variables → Actions**:

| 이름 | 값 |
|---|---|
| `SUPABASE_ACCESS_TOKEN` | dash.supabase.com → Account → Access Tokens 에서 발급 |
| `SUPABASE_PROJECT_REF` | 프로젝트 Settings → General → Reference ID |

**B. 함수 시크릿 (Supabase)**

대시보드 **Edge Functions → Secrets** 또는 CLI:

```bash
supabase secrets set PROXY_TOKEN=$(openssl rand -hex 24) --project-ref <REF>
```

**C. 배포 & URL 확보**

`index.ts` 푸시(또는 deploy-proxy 워크플로우 수동 실행)하면 배포된다. 함수 URL:

```
https://<REF>.supabase.co/functions/v1/union-proxy
```

## 배포 후 검증 (Supabase가 union에 닿는지)

```bash
curl -X POST 'https://<REF>.supabase.co/functions/v1/union-proxy/Ajax/Bible/BodyTop' \
  -H 'x-proxy-token: <PROXY_TOKEN>' \
  --data "qt_ty=QT1&Base_de=$(date +%Y-%m-%d)"
```

→ union JSON(`BibleDay`...)이 나오면 성공. `502 upstream error`면 Supabase에서도
union에 못 닿는 것이므로 다른 경로(GitLab CI 등) 검토.

## 봇에 연결

리포 **Actions Secrets** 에 추가 (send-qt 워크플로우가 사용):

| 이름 | 값 |
|---|---|
| `UNION_BASE_URL` | `https://<REF>.supabase.co/functions/v1/union-proxy` |
| `UNION_PROXY_TOKEN` | 위 `PROXY_TOKEN`과 동일 |

설정되면 [`bansuk_bot/clients/union.py`](../../../bansuk_bot/clients/union.py)가 직접 호출
대신 이 프록시를 거친다. (미설정 시 직접 호출로 폴백)
