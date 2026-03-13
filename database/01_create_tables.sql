-- テーブルが存在する場合DROP
DROP TABLE IF EXISTS user_point_amounts;
DROP TABLE IF EXISTS notification_user_read_status;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS users;

-- ユーザ
CREATE TABLE IF NOT EXISTS users
(
    id                          bigserial PRIMARY KEY,
    user_code                   varchar(10) UNIQUE                    NOT NULL,
    token                       varchar(36) DEFAULT NULL,
    card_code                   varchar(3)  DEFAULT NULL,
    card_brand                  varchar(1)  DEFAULT NULL,
    card_grade                  varchar(2)  DEFAULT NULL,
    created_at                  timestamp   DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                  timestamp   DEFAULT NULL
);
COMMENT ON TABLE users IS 'ユーザ';
COMMENT ON COLUMN users.id IS 'ID';
COMMENT ON COLUMN users.user_code IS 'ユーザコード';
COMMENT ON COLUMN users.tokein IS 'トークン';
COMMENT ON COLUMN users.card_code IS 'カード会社コード';
COMMENT ON COLUMN users.card_brand IS 'カードブランド';
COMMENT ON COLUMN users.card_grade IS 'カードグレード';
COMMENT ON COLUMN users.created_at IS '登録日時';
COMMENT ON COLUMN users.updated_at IS '更新日時';

-- お知らせ
CREATE TABLE IF NOT EXISTS notifications
(
    id                     bigserial PRIMARY KEY,
    notification_status    varchar(20) NOT NULL,
    is_push                bool        NOT NULL DEFAULT false,
    push_message           text                 DEFAULT NULL,
    is_push_set            bool        NOT NULL DEFAULT false,
    push_send_at           timestamp            DEFAULT NULL,
    thumbnail_path         text                 DEFAULT NULL,
    detail_image_path      text                 DEFAULT NULL,
    title                  text                 DEFAULT NULL,
    content_body           text                 DEFAULT NULL,
    link_url               text                 DEFAULT NULL,
    publication_start_date bigint               DEFAULT NULL,
    publication_end_date   bigint               DEFAULT NULL,
    action                 varchar(6)  NOT NULL DEFAULT 'detail',
    open_by                varchar(7)  NOT NULL DEFAULT 'webview',
    is_visible             bool        NOT NULL default true,
    created_at             timestamp            DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at             timestamp            DEFAULT NULL
);
COMMENT ON TABLE notifications IS 'お知らせ';
COMMENT ON COLUMN notifications.id IS 'ID';
COMMENT ON COLUMN notifications.notification_status IS 'お知らせステータス: 下書き保存、承認待ち、承認済、否認、取消';
COMMENT ON COLUMN notifications.is_push IS 'Push通知フラグ';
COMMENT ON COLUMN notifications.push_message IS 'Pushメッセージ';
COMMENT ON COLUMN notifications.is_push_set IS 'Push通知グループ設定登録フラグ';
COMMENT ON COLUMN notifications.push_send_at IS 'PUsh送信日時';
COMMENT ON COLUMN notifications.thumbnail_path IS 'お知らせ一覧画像パス';
COMMENT ON COLUMN notifications.detail_image_path IS 'お知らせ詳細画像パス';
COMMENT ON COLUMN notifications.title IS 'タイトル';
COMMENT ON COLUMN notifications.content_body IS 'コンテンツ本文';
COMMENT ON COLUMN notifications.link_url IS '遷移先URL';
COMMENT ON COLUMN notifications.publication_start_date IS '掲載開始日時';
COMMENT ON COLUMN notifications.publication_end_date IS '掲載終了日時';
COMMENT ON COLUMN notifications.is_visible IS '表示フラグ';
COMMENT ON COLUMN notifications.created_at IS '登録日時';
COMMENT ON COLUMN notifications.updated_at IS '更新日時';

-- お知らせ既読状況
CREATE TABLE IF NOT EXISTS notification_user_read_status
(
    user_id                     bigint,
    notification_id             bigint,
    read_at                     bigint    DEFAULT NULL,
    created_at                  timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                  timestamp DEFAULT NULL,
    PRIMARY KEY (user_id, notification_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (notification_id) REFERENCES notifications (id)
);
COMMENT ON TABLE notification_user_read_status IS 'お知らせ既読状況';
COMMENT ON COLUMN notification_user_read_status.user_id IS 'ユーザID';
COMMENT ON COLUMN notification_user_read_status.notification_id IS 'お知らせID';
COMMENT ON COLUMN notification_user_read_status.read_at IS 'お知らせ開封日時';
COMMENT ON COLUMN notification_user_read_status.created_at IS '登録日時';
COMMENT ON COLUMN notification_user_read_status.updated_at IS '更新日時';

-- 参考: ポイント残高
CREATE TABLE IF NOT EXISTS user_point_amounts
(
    user_id                     bigint,
    point_amount                bigint,
    created_at                  timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at                  timestamp DEFAULT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
COMMENT ON TABLE user_point_amounts IS 'ユーザポイント残高';
COMMENT ON COLUMN user_point_amounts.user_id IS 'ユーザID';
COMMENT ON COLUMN user_point_amounts.point_amount IS 'ポイント残高';
COMMENT ON COLUMN user_point_amounts.created_at IS '登録日時';
COMMENT ON COLUMN user_point_amounts.updated_at IS '更新日時';