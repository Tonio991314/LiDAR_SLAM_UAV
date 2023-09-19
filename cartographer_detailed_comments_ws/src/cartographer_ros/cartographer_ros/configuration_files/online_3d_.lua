include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
-- 下面两个frame需要修改为雷达的 坐标系，通常为laser
-- 如果有imu 需要将 tracking_frame 更改为 imu的那个link
  tracking_frame = "imu_link",  
  published_frame = "imu_link",
  odom_frame = "odom",
  provide_odom_frame = true,
  publish_frame_projected_to_2d = false,
  use_pose_extrapolator = true,

  use_odometry = false,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 0,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 1,

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

MAP_BUILDER.use_trajectory_builder_3d = true
   TRAJECTORY_BUILDER_2D.use_imu_data = true
   TRAJECTORY_BUILDER_3D.num_accumulated_range_data = 1
   TRAJECTORY_BUILDER_3D.min_range = 0.3
  --  defualt 60 
   TRAJECTORY_BUILDER_3D.max_range = 5.
   TRAJECTORY_BUILDER_2D.min_z = 0.1
   TRAJECTORY_BUILDER_2D.max_z = 1.0
   TRAJECTORY_BUILDER_3D.use_online_correlative_scan_matching = false
MAP_BUILDER.num_background_threads = 8  -- 后端的线条数，越大实时性越好
   POSE_GRAPH.optimization_problem.huber_scale = 5e2

  -- 设置为0，关闭global slam （取消后端优化，此时再出现建图问题就是前端的锅了）
  -- default:60 
   POSE_GRAPH.optimize_every_n_nodes = 320   -- 多少个点优化一次  越小优化频率越高

   POSE_GRAPH.constraint_builder.sampling_ratio = 0.03  
   POSE_GRAPH.optimization_problem.ceres_solver_options.max_num_iterations = 10
   POSE_GRAPH.constraint_builder.min_score = 0.6
   POSE_GRAPH.constraint_builder.global_localization_min_score = 0.60

   POSE_GRAPH.optimization_problem.odometry_translation_weight = 1e3
   POSE_GRAPH.optimization_problem.odometry_rotation_weight = 1e3
   
   POSE_GRAPH.constraint_builder.log_matches = true
   POSE_GRAPH.optimization_problem.log_solver_summary = true

return options