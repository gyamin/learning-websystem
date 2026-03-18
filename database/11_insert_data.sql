INSERT INTO users (
    user_code,
    token,
    card_code,
    card_brand,
    card_grade,
    updated_at
) VALUES
    ('1000000001', '11111111-1111-1111-1111-111111111111', '001', 'V', '1', NULL),
    ('1000000002', '22222222-2222-2222-2222-222222222222', '002', 'M', '2', NULL),
    ('1000000003', '33333333-3333-3333-3333-333333333333', '001', 'J', '3', NULL),
    ('1000000004', '44444444-4444-4444-4444-444444444444', '002', 'V', '1', NULL),
    ('1000000005', '55555555-5555-5555-5555-555555555555', '001', 'M', '2', NULL),
    ('1000000006', '66666666-6666-6666-6666-666666666666', '002', 'J', '3', NULL),
    ('1000000007', '77777777-7777-7777-7777-777777777777', '001', 'V', '2', NULL),
    ('1000000008', '88888888-8888-8888-8888-888888888888', '002', 'M', '3', NULL),
    ('1000000009', '99999999-9999-9999-9999-999999999999', '001', 'J', '1', NULL),
    ('1000000010', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '002', 'V', '2', NULL);


INSERT INTO notifications (
    notification_status,
    is_push,
    push_message,
    is_push_set,
    push_send_at,
    thumbnail_path,
    detail_image_path,
    title,
    content_body,
    link_url,
    publication_start_date,
    publication_end_date,
    action,
    open_by,
    is_visible,
    updated_at
) VALUES
    (
        '承認済',
        true,
        '12/18メンテナンスのお知らせ',
        true,
        CURRENT_TIMESTAMP,
        '/images/notifications/thumb_001.png',
        '/images/notifications/detail_001.png',
        '12/18にメンテナンスを実施します',
        'システムメンテナンスを実施します。詳細をご確認ください。',
        'https://example.local/notifications/1',
        TIMESTAMP '2026-03-10 09:00:00',
        TIMESTAMP '2026-03-31 23:59:59',
        'detail',
        'webview',
        true,
        NULL
    ),
    (
        '承認済',
        false,
        NULL,
        false,
        NULL,
        '/images/notifications/thumb_002.png',
        '/images/notifications/detail_002.png',
        'キャンペーン開始',
        '期間限定キャンペーンを開始しました。ぜひご利用ください。',
        'https://example.local/notifications/2',
        TIMESTAMP '2026-03-11 09:00:00',
        TIMESTAMP '2026-04-10 23:59:59',
        'detail',
        'webview',
        true,
        NULL
    ),
    (
        '下書き保存',
        false,
        NULL,
        false,
        NULL,
        '/images/notifications/thumb_003.png',
        '/images/notifications/detail_003.png',
        '新機能リリース予定',
        '近日中に新機能を公開予定です。',
        'https://example.local/notifications/3',
        TIMESTAMP '2026-03-15 09:00:00',
        TIMESTAMP '2026-04-15 23:59:59',
        'detail',
        'webview',
        true,
        NULL
    ),
    (
        '承認済',
        true,
        '重要なお知らせを公開しました',
        true,
        CURRENT_TIMESTAMP,
        '/images/notifications/thumb_004.png',
        '/images/notifications/detail_004.png',
        '利用規約改定のお知らせ',
        '利用規約を一部改定しました。内容をご確認ください。',
        'https://example.local/notifications/4',
        TIMESTAMP '2026-03-12 09:00:00',
        TIMESTAMP '2026-05-31 23:59:59',
        'detail',
        'webview',
        true,
        NULL
    ),
    (
        '否認',
        false,
        NULL,
        false,
        NULL,
        '/images/notifications/thumb_005.png',
        '/images/notifications/detail_005.png',
        '終了したキャンペーン',
        '本キャンペーンは終了しました。',
        'https://example.local/notifications/5',
        TIMESTAMP '2026-02-01 09:00:00',
        TIMESTAMP '2026-02-28 23:59:59',
        'detail',
        'webview',
        false,
        NULL
    );

-- CMSユーザ
-- パスワードはsha256でハッシュ化
-- '53a323910d6acb126eadc61d22e9f952678dfb86c2f0470d2aa0dbddd284e67a' : passa000001
-- '812a92c499257abe0ed680320947615a3525e80dba71e3a574ebe6d71b8a0044' : passb000001
-- '14ddfecd8f974f8dc998e070d6dbaf069b6474a7f9e9145a309c9fe30c5d67d3' : passc000001
INSERT INTO cms_users (
    login_id,
    login_password,
    user_name,
    user_type,
    created_at,
    updated_at
) VALUES
    ('A000001', '53a323910d6acb126eadc61d22e9f952678dfb86c2f0470d2aa0dbddd284e67a', '山本 美穂', 'admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('B000001', '812a92c499257abe0ed680320947615a3525e80dba71e3a574ebe6d71b8a0044', '鈴木 一郎', 'editor', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('C000001', '14ddfecd8f974f8dc998e070d6dbaf069b6474a7f9e9145a309c9fe30c5d67d3', '中村 大輔', 'operator', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);