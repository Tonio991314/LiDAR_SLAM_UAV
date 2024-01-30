include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
-- 下面两个frame需要修改为雷达的 坐标系，通常为laser
-- 如果有imu 需要将 tracking_frame 更改为 imu的那个link
  tracking_frame = "imu_link",  
  published_frame = "base_link",  
  odom_frame = "odom",
  provide_odom_frame = false,
  publish_frame_projected_to_2d = false,
  use_pose_extrapolator = true,

  use_odometry = false,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1, -- 1: use laser scan
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0, -- 1: use point cloud

  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 8.
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 5.
TRAJECTORY_BUILDER_2D.use_imu_data = true
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.01)
TRAJECTORY_BUILDER_2D.motion_filter.max_distance_meters = 20
TRAJECTORY_BUILDER_2D.motion_filter.max_time_seconds = 1
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight = 0.01
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.rotation_weight = 0.01


POSE_GRAPH.constraint_builder.min_score = 0.65
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7

return options