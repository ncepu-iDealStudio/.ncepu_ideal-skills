/// 数据模型：技能
///
/// 字段与后端接口保持一致，避免对接时改动页面。
class Skill {
  const Skill({
    required this.id,
    required this.title,
    required this.userName,
    this.avatar = '',
    this.tags = const [],
    this.wantTags = const [],
    this.rating = 0,
    this.swapCount = 0,
    this.description = '',
  });

  final int id;
  final String title;
  final String userName;

  /// 头像地址，空字符串表示无头像
  final String avatar;

  /// 我会的技能标签
  final List<String> tags;

  /// 我想学的技能标签
  final List<String> wantTags;

  /// 评分 0-5
  final double rating;

  /// 已成功互换次数
  final int swapCount;

  /// 补充说明
  final String description;

  /// 从后端 JSON 构造。字段缺失时给出安全默认值，避免运行时报错。
  factory Skill.fromJson(Map<String, dynamic> json) {
    return Skill(
      id: (json['id'] as num?)?.toInt() ?? 0,
      title: (json['title'] as String?) ?? '',
      userName: (json['userName'] as String?) ?? '',
      avatar: (json['avatar'] as String?) ?? '',
      tags: (json['tags'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList(growable: false) ??
          const [],
      wantTags: (json['wantTags'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList(growable: false) ??
          const [],
      rating: (json['rating'] as num?)?.toDouble() ?? 0,
      swapCount: (json['swapCount'] as num?)?.toInt() ?? 0,
      description: (json['description'] as String?) ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'userName': userName,
      'avatar': avatar,
      'tags': tags,
      'wantTags': wantTags,
      'rating': rating,
      'swapCount': swapCount,
      'description': description,
    };
  }
}
