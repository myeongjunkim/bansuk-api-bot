// 성서유니온(sum.su.or.kr:8888) 전용 얇은 프록시 — Supabase Edge Function.
//
// 배경: GitHub Actions(Azure) egress IP가 union 서버에 간헐적으로 차단된다.
// Supabase Edge Function은 Deno 런타임(비-Azure, 임의 포트 8888 outbound 허용)이라
// 여기를 거쳐 호출하면 차단을 우회한다.
//   GitHub Actions ──> 이 함수 ──> sum.su.or.kr:8888
//
// 호출 예: https://<ref>.supabase.co/functions/v1/union-proxy/Ajax/Bible/BodyTop
// 인증: x-proxy-token 헤더가 PROXY_TOKEN 과 일치해야 함 (verify_jwt=false).

const UPSTREAM = "https://sum.su.or.kr:8888";
const TOKEN = Deno.env.get("PROXY_TOKEN");

Deno.serve(async (req: Request): Promise<Response> => {
  const url = new URL(req.url);
  // Supabase는 /functions/v1/union-proxy 접두사를 포함해 전달하므로 떼어내
  // union의 실제 경로(/Ajax/...)만 추출한다.
  const path = url.pathname
    .replace(/^\/functions\/v1/, "")
    .replace(/^\/union-proxy/, "");

  // 헬스체크
  if (path === "" || path === "/") {
    return new Response("ok", { status: 200 });
  }

  // 오픈 릴레이 방지용 공유 토큰
  if (!TOKEN || req.headers.get("x-proxy-token") !== TOKEN) {
    return new Response("forbidden", { status: 403 });
  }

  try {
    const upstream = await fetch(UPSTREAM + path, {
      method: req.method,
      headers: {
        "content-type":
          req.headers.get("content-type") ??
          "application/x-www-form-urlencoded",
      },
      body:
        req.method === "GET" || req.method === "HEAD"
          ? undefined
          : await req.arrayBuffer(),
    });

    return new Response(await upstream.arrayBuffer(), {
      status: upstream.status,
      headers: {
        "content-type":
          upstream.headers.get("content-type") ?? "application/json",
      },
    });
  } catch (err) {
    return new Response(`upstream error: ${err}`, { status: 502 });
  }
});
