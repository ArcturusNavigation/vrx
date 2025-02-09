import xml.etree.ElementTree as ET

def create_buoy(name, x, y, color):
    # Create an <include> tag for a buoy
    include = ET.Element("include")

    # Add <name> tag
    name_tag = ET.SubElement(include, "name")
    name_tag.text = name

    # Add <pose> tag
    pose_tag = ET.SubElement(include, "pose")
    pose_tag.text = f"{x} {y} 1.720474 -0.004994 0.020798 1.301492"

    # Add <uri> tag
    uri_tag = ET.SubElement(include, "uri")
    uri_tag.text = f"round_buoy_{color}"

    # Add <plugin> tag
    plugin = ET.SubElement(include, "plugin", name="vrx::PolyhedraBuoyancyDrag", filename="libPolyhedraBuoyancyDrag.so")

    ET.SubElement(plugin, "fluid_density").text = "1000"
    ET.SubElement(plugin, "fluid_level").text = "0.0"
    ET.SubElement(plugin, "linear_drag").text = "25.0"
    ET.SubElement(plugin, "angular_drag").text = "2.0"

    buoyancy = ET.SubElement(plugin, "buoyancy", name="collision_outer")
    ET.SubElement(buoyancy, "link_name").text = "link"
    ET.SubElement(buoyancy, "pose").text = "0 0 -0.3 0 0 0"

    geometry = ET.SubElement(buoyancy, "geometry")
    cylinder = ET.SubElement(geometry, "cylinder")
    ET.SubElement(cylinder, "radius").text = "0.325"
    ET.SubElement(cylinder, "length").text = "0.1"

    wavefield = ET.SubElement(plugin, "wavefield")
    ET.SubElement(wavefield, "topic").text = "/vrx/wavefield/parameters"

    return include


def generate_gazebo_world(coordinates, file_path):
    # Static header to include at the beginning of the world file
    # Extract the world name from the file name
    world_name = file_path.split("/")[-1].replace(".sdf", "").replace(" ", "_")
    print("world name???", world_name)
    
    header = f'''
    <?xml version="1.0" ?>

<sdf version="1.9">
  <world name="{world_name}">

    <physics name="4ms" type="dart">
      <max_step_size>0.004</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <gui fullscreen="0">

      <!-- 3D scene -->
      <plugin filename="MinimalScene" name="3D View">
        <gz-gui>
          <title>3D View</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="string" key="state">docked</property>
        </gz-gui>

        <engine>ogre2</engine>
        <scene>scene</scene>
        <ambient_light>0.4 0.4 0.4</ambient_light>
        <background_color>0.8 0.8 0.8</background_color>
        <camera_pose>-478.1 148.2 13.2 0 0.25 2.94</camera_pose>
        <camera_clip>
          <near>0.25</near>
          <far>10000</far>
        </camera_clip>
      </plugin>

      <!-- Plugins that add functionality to the scene -->
      <plugin filename="EntityContextMenuPlugin" name="Entity context menu">
        <gz-gui>
          <property key="state" type="string">floating</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="GzSceneManager" name="Scene Manager">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="InteractiveViewControl" name="Interactive view control">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="CameraTracking" name="Camera Tracking">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="MarkerManager" name="Marker manager">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="SelectEntities" name="Select Entities">
        <gz-gui>
          <anchors target="Select entities">
            <line own="right" target="right"/>
            <line own="top" target="top"/>
          </anchors>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="VisualizationCapabilities" name="Visualization Capabilities">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>

      <plugin filename="Spawn" name="Spawn Entities">
        <gz-gui>
          <anchors target="Select entities">
            <line own="right" target="right"/>
            <line own="top" target="top"/>
          </anchors>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>

      <!-- World control -->
      <plugin filename="WorldControl" name="World control">
        <gz-gui>
          <title>World control</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="bool" key="resizable">false</property>
          <property type="double" key="height">72</property>
          <property type="double" key="width">121</property>
          <property type="double" key="z">1</property>

          <property type="string" key="state">floating</property>
          <anchors target="3D View">
            <line own="left" target="left"/>
            <line own="bottom" target="bottom"/>
          </anchors>
        </gz-gui>

        <play_pause>true</play_pause>
        <step>true</step>
        <start_paused>true</start_paused>
        <use_event>true</use_event>

      </plugin>

      <!-- World statistics -->
      <plugin filename="WorldStats" name="World stats">
        <gz-gui>
          <title>World stats</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="bool" key="resizable">false</property>
          <property type="double" key="height">110</property>
          <property type="double" key="width">290</property>
          <property type="double" key="z">1</property>

          <property type="string" key="state">floating</property>
          <anchors target="3D View">
            <line own="right" target="right"/>
            <line own="bottom" target="bottom"/>
          </anchors>
        </gz-gui>

        <sim_time>true</sim_time>
        <real_time>true</real_time>
        <real_time_factor>true</real_time_factor>
        <iterations>true</iterations>
      </plugin>

      <!-- Insert simple shapes -->
      <plugin filename="Shapes" name="Shapes">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="x" type="double">0</property>
          <property key="y" type="double">0</property>
          <property key="width" type="double">250</property>
          <property key="height" type="double">50</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
          <property key="cardBackground" type="string">#666666</property>
        </gz-gui>
      </plugin>

      <!-- Insert lights -->
      <plugin filename="Lights" name="Lights">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="x" type="double">250</property>
          <property key="y" type="double">0</property>
          <property key="width" type="double">150</property>
          <property key="height" type="double">50</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
          <property key="cardBackground" type="string">#666666</property>
        </gz-gui>
      </plugin>

      <!-- Translate / rotate -->
      <plugin filename="TransformControl" name="Transform control">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="x" type="double">0</property>
          <property key="y" type="double">50</property>
          <property key="width" type="double">250</property>
          <property key="height" type="double">50</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
          <property key="cardBackground" type="string">#777777</property>
        </gz-gui>

        <!-- disable legacy features used to connect this plugin to GzScene3D -->
        <legacy>false</legacy>
      </plugin>

      <!-- Screenshot -->
      <plugin filename="Screenshot" name="Screenshot">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="x" type="double">250</property>
          <property key="y" type="double">50</property>
          <property key="width" type="double">50</property>
          <property key="height" type="double">50</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
          <property key="cardBackground" type="string">#777777</property>
        </gz-gui>
      </plugin>

      <!-- Video recorder -->
      <plugin filename="VideoRecorder" name="VideoRecorder">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="x" type="double">300</property>
          <property key="y" type="double">50</property>
          <property key="width" type="double">50</property>
          <property key="height" type="double">50</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
          <property key="cardBackground" type="string">#777777</property>
        </gz-gui>

        <record_video>
          <use_sim_time>true</use_sim_time>
          <lockstep>true</lockstep>
          <bitrate>4000000</bitrate>
        </record_video>

        <!-- disable legacy features used to connect this plugin to GzScene3D -->
        <legacy>false</legacy>
      </plugin>

      <!-- Inspector -->
      <plugin filename="ComponentInspector" name="Component inspector">
        <gz-gui>
          <property type="string" key="state">docked_collapsed</property>
        </gz-gui>
      </plugin>

      <!-- Entity tree -->
      <plugin filename="EntityTree" name="Entity tree">
        <gz-gui>
          <property type="string" key="state">docked_collapsed</property>
        </gz-gui>
      </plugin>

      <!-- View angle -->
      <plugin filename="ViewAngle" name="View angle">
        <gz-gui>
          <property type="string" key="state">docked_collapsed</property>
        </gz-gui>

        <!-- disable legacy features used to connect this plugin to GzScene3D -->
        <legacy>false</legacy>
      </plugin>

    </gui>

    <plugin
      filename="gz-sim-physics-system"
      name="gz::sim::systems::Physics">
    </plugin>
    <plugin
      filename="gz-sim-user-commands-system"
      name="gz::sim::systems::UserCommands">
    </plugin>
    <plugin
      filename="gz-sim-sensors-system"
      name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
      <disable_on_drained_battery>true</disable_on_drained_battery>
    </plugin>
    <plugin
      filename="gz-sim-imu-system"
      name="gz::sim::systems::Imu">
    </plugin>
    <plugin
      filename="gz-sim-magnetometer-system"
      name="gz::sim::systems::Magnetometer">
    </plugin>
    <plugin
      filename="gz-sim-forcetorque-system"
      name="gz::sim::systems::ForceTorque">
    </plugin>
    <plugin
      filename="gz-sim-particle-emitter2-system"
      name="gz::sim::systems::ParticleEmitter2">
    </plugin>
    <plugin
      filename="gz-sim-scene-broadcaster-system"
      name="gz::sim::systems::SceneBroadcaster">
    </plugin>
    <plugin
      filename="gz-sim-contact-system"
      name="gz::sim::systems::Contact">
    </plugin>
    <plugin
      filename="gz-sim-navsat-system"
      name="gz::sim::systems::NavSat">
    </plugin>
    <scene>
      <sky></sky>
      <grid>false</grid>
      <ambient>1.0 1.0 1.0</ambient>
      <background>0.8 0.8 0.8</background>
    </scene>

    <!-- Estimated latitude/longitude of sydneyregatta
         from satellite imagery -->
    <spherical_coordinates>
      <surface_model>EARTH_WGS84</surface_model>
      <world_frame_orientation>ENU</world_frame_orientation>
      <latitude_deg>-33.724223</latitude_deg>
      <longitude_deg>150.679736</longitude_deg>
      <elevation>0.0</elevation>
      <heading_deg>0.0</heading_deg>
    </spherical_coordinates>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <include>
      <pose> 0 0 0.2 0 0 0 </pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/sydney_regatta</uri>
    </include>

    <include>
      <name>Coast Waves</name>
      <pose>0 0 0 0 0 0</pose>
      <uri>coast_waves</uri>
    </include>

    <include>
      <name>platform</name>
      <uri>platform</uri>
    </include>
    '''

    # Static footer to include at the end of the world file
    footer = '''
<!-- <?xml version='1.0' encoding='utf-8'?>
<sdf version="1.6"><model name="adjusted_navigation_course"> -->
    
    <!-- </model></sdf> -->

    <!-- The posts for securing the WAM-V -->
    <include>
      <name>post_0</name>
      <pose>-535.916809 154.362869 0.675884 -0.17182 0.030464 -0.005286</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/post</uri>
    </include>
    <include>
      <name>post_1</name>
      <pose>-527.48999 153.854782 0.425844 -0.1365 0  0</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/post</uri>
    </include>
    <include>
      <name>post_2</name>
      <pose>-544.832825 156.671951 0.499025 -0.162625 0 0 </pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/post</uri>
    </include>

    <!-- Antenna for communication with the WAM-V -->
    <include>
      <pose>-531.063721 147.668579 1.59471 -0.068142 0 -0.1</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/antenna</uri>
    </include>

    <!-- ground station tents -->
    <include>
      <name>ground_station_0</name>
      <pose>-540.796448 146.493744 1.671421 -0.00834 0.01824 1.301726</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/ground_station</uri>
    </include>
    <include>
      <name>ground_station_1</name>
      <pose>-537.622681 145.827896 1.681931 -0.00603 0.018667 1.301571</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/ground_station</uri>
    </include>
    <include>
      <name>ground_station_2</name>
      <pose>-534.550537 144.910400 1.720474 -0.004994 0.020798 1.301492</pose>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/ground_station</uri>
    </include>

    <!-- The projectile for the ball shooter -->
    <include>
      <name>blue_projectile</name>
      <pose>-545 60 0.03 0 0 0</pose>
      <uri>blue_projectile</uri>
      <plugin name="vrx::PolyhedraBuoyancyDrag"
              filename="libPolyhedraBuoyancyDrag.so">
        <fluid_density>1000</fluid_density>
        <fluid_level>0.0</fluid_level>
        <linear_drag>25.0</linear_drag>
        <angular_drag>2.0</angular_drag>
        <buoyancy name="collision_outer">
          <link_name>link</link_name>
          <pose>0 0 -0.02 0 0 0</pose>
          <geometry>
            <sphere>
              <radius>0.0285</radius>
            </sphere>
          </geometry>
        </buoyancy>
        <wavefield>
          <topic>/vrx/wavefield/parameters</topic>
        </wavefield>
      </plugin>
    </include>

    <!-- Load the plugin for the wind -->
    <plugin
      filename="libUSVWind.so"
      name="vrx::USVWind">
      <!-- models to be effected by the wind -->
      <wind_obj>
        <name>wamv</name>
        <link_name>wamv/base_link</link_name>
        <coeff_vector> .5 .5 .33</coeff_vector>
      </wind_obj>
      <!-- Wind -->
      <wind_direction>355</wind_direction>
      <!-- in degrees -->
      <wind_mean_velocity>9.0</wind_mean_velocity>
      <var_wind_gain_constants>5.0</var_wind_gain_constants>
      <var_wind_time_constants>2</var_wind_time_constants>
      <random_seed>19</random_seed>
      <!-- set to zero/empty to randomize -->
      <update_rate>10</update_rate>
      <topic_wind_speed>/vrx/debug/wind/speed</topic_wind_speed>
      <topic_wind_direction>/vrx/debug/wind/direction</topic_wind_direction>
    </plugin>

    <!-- Scoring Plugin -->
    <plugin
      filename="libNavigationScoringPlugin.so"
      name="vrx::NavigationScoringPlugin">
      <vehicle>wamv</vehicle>
      <task_name>follow_path</task_name>
      <task_info_topic>/vrx/task/info</task_info_topic>
      <contact_debug_topic>/vrx/follow_path/debug/contact</contact_debug_topic>
      <initial_state_duration>10</initial_state_duration>
      <ready_state_duration>10</ready_state_duration>
      <running_state_duration>300</running_state_duration>
      <collision_buffer>10</collision_buffer>
      <release_topic>/vrx/release</release_topic>

      <course_name>short_navigation_course_2</course_name>
      <points_per_gate_crossed>10</points_per_gate_crossed>
      <obstacle_penalty>3.0</obstacle_penalty>
      <bonus>1</bonus>
      <gates>
        <gate>
          <left_marker>red_bound_0</left_marker>
          <right_marker>green_bound_0</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_1</left_marker>
          <right_marker>green_bound_1</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_2</left_marker>
          <right_marker>green_bound_2</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_3</left_marker>
          <right_marker>green_bound_3</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_4</left_marker>
          <right_marker>green_bound_4</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_5</left_marker>
          <right_marker>green_bound_5</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_6</left_marker>
          <right_marker>green_bound_6</right_marker>
        </gate>
        <gate>
          <left_marker>red_bound_7</left_marker>
          <right_marker>green_bound_7</right_marker>
        </gate>
         <gate>
          <left_marker>red_bound_8</left_marker>
          <right_marker>green_bound_8</right_marker>
        </gate>
     </gates>
    </plugin>

    <!-- The wave field -->
    <plugin filename="libPublisherPlugin.so" name="vrx::PublisherPlugin">
      <message type="gz.msgs.Param" topic="/vrx/wavefield/parameters"
               every="2.0">
        params {
          key: "direction"
          value {
            type: DOUBLE
            double_value: 0.0
          }
        }
        params {
          key: "gain"
          value {
            type: DOUBLE
            double_value: 2.0
          }
        }
        params {
          key: "period"
          value {
            type: DOUBLE
            double_value: 2.0
          }
        }
        params {
          key: "steepness"
          value {
            type: DOUBLE
            double_value: 0
          }
        }
      </message>
    </plugin>
  </world>
</sdf>
'''

    

    # Start writing the world file
    world_content = header

    # Track count of each color for unique naming
    color_count = {"red": 0, "yellow": 0, "green": 0}

    # Iterate through coordinates and add buoys
    for x, y, color in coordinates:
        color_count[color] += 1
        buoy_name = f"round_buoy_{color}_{color_count[color]}"
        buoy_element = create_buoy(buoy_name, x, y, color)
        world_content += ET.tostring(buoy_element, encoding='unicode')

    # Append the footer
    world_content += footer

    # Write the final content to the specified file path
    with open(file_path, "w") as f:
        f.write(world_content)

if __name__ == "__main__":
    
    # TO DO: Define locations and colors of round buoys
    # Formst: list of (x, y, color)
    coordinates = [
        (-537.55, 175.91, "red"),
        (-538.11, 175.91, "yellow"),
        (-543.55, 175.91, "green"),
        (-536.55, 180.91, "red"),
        (-541.05, 181.91, "yellow"),
        (-542.55, 180.91, "green")
    ]

    # TO DO: Define the output file path and name
    file_path = "vrx_gz/worlds/rb2025/example_generated_world.sdf"

    # Generate the world file
    generate_gazebo_world(coordinates, file_path)

    print(f"Gazebo world file created successfully at {file_path}.")
