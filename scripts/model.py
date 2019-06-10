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
#cd("/")
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

#cd("/")
#create(dsname, 'JDBCSystemResource')
#cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
#cmo.setName(dsname)

cd("/")
create(dsname, 'JDBCSystemResource')
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
cmo.setName(dsname)

create('myJdbcDataSourceParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', java.lang.String(dsjndiname))
set('GlobalTransactionsProtocol', java.lang.String('None'))

print 'create JDBCDriverParams'
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
create('myJdbcDriverParams','JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('DriverName', dsdriver)
set('URL', dsurl)
set('PasswordEncrypted', dspassword)
set('UseXADataSourceInterface', 'true')


print 'create JDBCConnectionPoolParams'
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname)
create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('InitialCapacity', 0)
set('MaxCapacity', 25)
set('TestTableName', "SQL ISVALID")

print 'create JDBCDriverParams Properties'
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname + '/JdbcDriverParams/' + dsname)
#create('myProperties','Properties')
#cd('Properties/NO_NAME_0')

print 'ls (a)'
ls('a')
print "---"
print 'ls (c)'
ls('c')
print "---"
cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname + '/JdbcDriverParams/' + dsname + '/Properties/' + dsname )
cmo.createProperty("javax.net.ssl.keyStoreType")

cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname + '/JdbcDriverParams/' + dsname + '/Properties/' + dsname + "/Property/javax.net.ssl.keyStoreType")
cmo.setValue("JKS")






cd('/JDBCSystemResource/' + dsname + '/JdbcResource/' + dsname + '/Properties/' + dsname)
create('myProperties','Properties')
cd('Properties/NO_NAME_0')
create('user','Property')
cd('Property/user')
set('Value', dsusername)

cd ("../")
create('oracle.jdbc.fanEnabled','Property')
cd('Property/oracle.jdbc.fanEnabled')
set('Value', "false")

cd ("../")
create('oracle.net.ssl_server_dn_match','Property')
cd('Property/oracle.net.ssl_server_dn_match')
set('Value', "true")

cd ("../")
create('oracle.net.tns_admin','Property')
cd('Property/oracle.net.tns_admin')
set('Value', db_wallet)

cd ("../")
create('oracle.net.ssl_version','Property')
cd('Property/oracle.net.ssl_version')
set('Value', "1.2")

cd ("../")
create('javax.net.ssl.keyStoreType','Property')
cd('Property/javax.net.ssl.keyStoreType')
set('Value', "JKS")

cd ("../")
create('javax.net.ssl.trustStoreType','Property')
cd('Property/javax.net.ssl.keyStoreType')
set('Value', "JKS")

cd ("../")
create('javax.net.ssl.trustStore','Property')
cd('Property/javax.net.ssl.trustStore')
set('Value', db_wallet + "/truststore.jks")

cd ("../")
create('javax.net.ssl.keyStore','Property')
cd('Property/javax.net.ssl.keyStore')
set('Value', db_wallet + "/keystore.jks")

cd ("../")
create('javax.net.ssl.trustStorePassword','Property')
cd('Property/javax.net.ssl.trustStorePassword')
set('Value', dspassword)

cd ("../")
create('javax.net.ssl.keyStorePassword','Property')
cd('Property/javax.net.ssl.keyStorePassword')
set('Value', dspassword)


#jdbcSR.addTarget(admin_server_name)
#jdbcSR.addTarget(cluster_name)


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
