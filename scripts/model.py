import os
from weblogic.management.configuration import TargetMBean

wl_home                  = os.environ.get("WL_HOME")
domain_path              = os.environ.get("DOMAIN_HOME")
domain_name              = "domain1"
username                 = "weblogic"
password                 = "welcome1"
admin_server_name        = "admin-server"
admin_port               = 7001
t3_channel_port          = 30012
t3_public_address        = "kubernetes"
cluster_name             = "cluster-1"
number_of_ms             = 5
managed_server_name_base = "managed-server"
managed_server_port      = 8001

db_wallet                = os.environ.get("DB_WALLET")

readTemplate(wl_home + "/common/templates/wls/wls.jar")

cmo.setName(domain_name)
setOption("DomainName", domain_name)
setOption("OverwriteDomain", "true")

cd("/Security/" + domain_name + "/User/weblogic")
cmo.setName(username)
cmo.setPassword(password)

cd("/Servers/AdminServer")
cmo.setListenPort(admin_port)
cmo.setName(admin_server_name)
nap=create("T3Channel", 'NetworkAccessPoint')
nap.setPublicPort(t3_channel_port)
nap.setPublicAddress(t3_public_address)
nap.setListenPort(t3_channel_port)

cd("/")
cl=create(cluster_name, 'Cluster')
templateName = cluster_name + "-template"
st=create(templateName, "ServerTemplate")
st.setListenPort(managed_server_port)
st.setCluster(cl)
cd("/Clusters/" + cluster_name)
ds=create(cluster_name, "DynamicServers")
ds.setServerTemplate(st)
ds.setServerNamePrefix(managed_server_name_base)
ds.setDynamicClusterSize(number_of_ms)
ds.setMaxDynamicClusterSize(number_of_ms)
ds.setCalculatedListenPorts(false)

# Create Datasource
# ==================
cd("/")
#create(dsname, 'JDBCSystemResource')
#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#cmo.setName(dsname)

#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcDataSourceParams','JDBCDataSourceParams')
#cd('JDBCDataSourceParams/NO_NAME_0')
#set('JNDIName', java.lang.String(dsjndiname))
#set('GlobalTransactionsProtocol', java.lang.String('None'))

#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcDriverParams','JDBCDriverParams')
#cd('JDBCDriverParams/NO_NAME_0')
#set('DriverName', dsdriver)
#set('URL', dsurl + db_wallet)
#set('PasswordEncrypted', dspassword)
#set('UseXADataSourceInterface', 'false')

#print 'create JDBCDriverParams Properties'
#create('myProperties','Properties')
#cd('Properties/NO_NAME_0')
#create('user','Property')
#cd('Property/user')
#set('Value', dsusername)

#print 'create JDBCConnectionPoolParams'
#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
#cd('JDBCConnectionPoolParams/NO_NAME_0')
#set('TestTableName','SQL SELECT 1 FROM DUAL')
#set('InitialCapacity', int(dsinitialcapacity))

# Assign
# ======
#assign('JDBCSystemResource', dsname, 'Target', admin_server_name)
#assign('JDBCSystemResource', dsname, 'Target', cluster_name)

print 'create JDBCDriverParams Properties'
cmo.createJDBCSystemResource(dsname)
theJDBCResource = cmo.lookupJDBCSystemResource(dsname)
#theJDBCResource = jdbcSR.getJDBCResource()

theJDBCResource.setName(dsname)

print 'create JDBCConnectionPoolParams'

connectionPoolParams = theJDBCResource.getJDBCConnectionPoolParams()
connectionPoolParams.setConnectionReserveTimeoutSeconds(25)
connectionPoolParams.setMaxCapacity(100)
connectionPoolParams.setTestTableName("SQL ISVALID")

dsParams = theJDBCResource.getJDBCDataSourceParams()
dsParams.addJNDIName(dsjndiname)

print 'create JDBCDriverParams'

driverParams = theJDBCResource.getJDBCDriverParams()
driverParams.setUrl()
driverParams.setDriverName(dsdriver)
driverParams.setPassword(dspassword)

driverProperties = driverParams.getProperties()
proper = driverProperties.createProperty("user")
proper.setValue(dsusername)
proper = driverProperties.createProperty("oracle.jdbc.fanEnabled")
proper.setValue("false")
proper = driverProperties.createProperty("oracle.net.ssl_server_dn_match")
proper.setValue("true")
proper = driverProperties.createProperty("oracle.net.tns_admin")
proper.setValue(db_wallet)
proper = driverProperties.createProperty("oracle.net.ssl_version")
proper.setValue("1.2")
# Use either the self-opening wallet
#proper.setValue(db_wallet)
# or uncomment and use the keyStore/trustStore, but not both
proper = driverProperties.createProperty("javax.net.ssl.keyStoreType")
proper.setValue("JKS")
proper = driverProperties.createProperty("javax.net.ssl.trustStoreType")
proper.setValue("JKS")
proper = driverProperties.createProperty("javax.net.ssl.trustStore")
proper.setValue(db_wallet + "/truststore.jks")
proper = driverProperties.createProperty("javax.net.ssl.trustStorePassword")
proper.setEncryptedValue(dspassword)
proper = driverProperties.createProperty("javax.net.ssl.keyStore")
proper.setValue(db_wallet + "/keytore.jks")
proper = driverProperties.createProperty("javax.net.ssl.keyStorePassword")
proper.setEncryptedValue(dspassword)

jdbcSR.addTarget(admin_server_name)
jdbcSR.addTarget(cluster_name)


# Deploy application
# ==========================
cd("/")
dep=create("testwebapp", "AppDeployment")
dep.setTargets(jarray.array([cl],TargetMBean))
dep.setModuleType("war")
dep.setSourcePath("wlsdeploy/applications/opdemo.war")

writeDomain(domain_path)
closeTemplate()

readDomain(domain_path)
cmo.setProductionModeEnabled(true)
updateDomain()
closeDomain()

exit()
