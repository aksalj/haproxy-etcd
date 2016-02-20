global
    log 127.0.0.1    local0
    log 127.0.0.1    local1 notice
    stats timeout 30s
    user aksalj

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000

    timeout check 3000
    default-server inter 10s fall 2 rise 1


listen stats
    bind *:8080
    mode http
    maxconn 1

    stats uri /
    stats refresh 30s

frontend http
    bind *:8081

    # Define hosts
    acl host_www hdr(host) -i www.aksalj.zr
    acl host_auth hdr(host) -i auth.aksalj.zr
    acl host_api hdr(host) -i api.aksalj.zr
    acl host_status hdr(host) -i status.aksalj.zr

    ## Each host with its backend
    use_backend auth if host_auth
    use_backend api if host_api
    use_backend status if host_status
    use_backend www if host_www

    default_backend www

backend www
    option forwardfor
    balance leastconn

    # Health check
    option httpchk GET /
    http-check expect status 200

    % for instance in instances['www']:
    server ${instance['name']} ${instance['host']}:${instance['port']} check
    % endfor

backend auth
    option forwardfor
    balance leastconn

    # Health check
    option httpchk GET /realms/master
    http-check expect status 200

    % for instance in instances['auth']:
    server ${instance['name']} ${instance['host']}:${instance['port']} check
    % endfor

backend api
    option forwardfor
    balance roundrobin

    # Health check
    option httpchk HEAD /_/health
    http-check expect status 200

    % for instance in instances['api']:
    server ${instance['name']} ${instance['host']}:${instance['port']} check
    % endfor

backend status
    option forwardfor
    balance roundrobin

    # Health check
    option httpchk GET /

    % for instance in instances['status']:
    server ${instance['name']} ${instance['host']}:${instance['port']} check
    % endfor