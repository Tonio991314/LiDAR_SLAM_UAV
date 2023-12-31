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
  use_pose_extrapolator = false,

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

  publish_tracked_pose = true,
}


MAP_BUILDER.use_trajectory_builder_3d = true
MAP_BUILDER.num_background_threads = 8


--LOCAL SLAM FIX FOR Z 

TRAJECTORY_BUILDER_3D.num_accumulated_range_data = 1
TRAJECTORY_BUILDER_3D.min_range = 2.5
TRAJECTORY_BUILDER_3D.max_range = 100
TRAJECTORY_BUILDER_3D.submaps.num_range_data = 150
TRAJECTORY_BUILDER_3D.voxel_filter_size = 0.1

-- TRAJECTORY_BUILDER_3D.motion_filter.max_angle_radians = math.rad(0.01)
-- TRAJECTORY_BUILDER_3D.motion_filter.max_distance_meters = 20
-- TRAJECTORY_BUILDER_3D.motion_filter.max_time_seconds = 1

TRAJECTORY_BUILDER_3D.use_online_correlative_scan_matching = true --true
TRAJECTORY_BUILDER_3D.real_time_correlative_scan_matcher.linear_search_window = 0.1
TRAJECTORY_BUILDER_3D.real_time_correlative_scan_matcher.translation_delta_cost_weight = 10.
TRAJECTORY_BUILDER_3D.real_time_correlative_scan_matcher.rotation_delta_cost_weight = 0.1

TRAJECTORY_BUILDER_3D.ceres_scan_matcher.translation_weight = 0.1
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.rotation_weight = 0.1
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.ceres_solver_options.max_num_iterations = 100


POSE_GRAPH.optimization_problem.log_solver_summary = true

-- GLOBAL_SLAM FIX FOR Z
-- POSE_GRAPH.optimization_problem.acceleration_weight = 500
-- POSE_GRAPH.optimization_problem.rotation_weight = 100

--Wait changing this really helped....find out why?

-- POSE_GRAPH.optimization_problem.acceleration_weight = 1e3
-- POSE_GRAPH.optimization_problem.rotation_weight = 3e5


POSE_GRAPH.optimization_problem.ceres_solver_options.max_num_iterations = 200
POSE_GRAPH.optimization_problem.huber_scale = 5e2
POSE_GRAPH.optimize_every_n_nodes = 32
POSE_GRAPH.constraint_builder.sampling_ratio = 0.1
POSE_GRAPH.global_sampling_ratio = 0.003
POSE_GRAPH.constraint_builder.min_score = 0.50
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.55

POSE_GRAPH.constraint_builder.max_constraint_distance = 20.
POSE_GRAPH.constraint_builder.fast_correlative_scan_matcher_3d.linear_xy_search_window = 50.
POSE_GRAPH.constraint_builder.fast_correlative_scan_matcher_3d.linear_z_search_window = 30.
POSE_GRAPH.constraint_builder.fast_correlative_scan_matcher_3d.angular_search_window = math.rad(60.)
POSE_GRAPH.constraint_builder.ceres_scan_matcher_3d.ceres_solver_options.max_num_iterations = 50


return options